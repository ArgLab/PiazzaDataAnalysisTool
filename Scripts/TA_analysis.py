import datetime
import numpy as np
import math
import spacy
from scipy.stats import ttest_ind, chi2_contingency, kruskal, chisqprob, chisquare
from ModSocDB.Classes.User import *
from ModSocDB.Classes.Piazza.PiazzaContent import *
from ModSocDB.Classes.Piazza.PiazzaContent_Child import *
from ModSocDB.Classes.Piazza.PiazzaContent_Child_Subchild import *

def load_posts(user):
    posts = PiazzaContent.query.find({'CentralAuthor_ID': user._id}).all()
    replies = PiazzaContent_Child.query.find({'CentralAuthor_ID': user._id}).all()
    reply_to_replies = PiazzaContent_Child_Subchild.query.find({'CentralAuthor_ID': user._id}).all()
    all_content = []
    for post in posts:
        if post.getLatestHistory() and post.getLatestHistory().content:
            all_content.append((post.created, 'post', post.getLatestHistory().content))
    for post in replies:
        if post.content:
            all_content.append((post.created, 'reply', post.content))
    for post in reply_to_replies:
        if post.content:
            all_content.append((post.created, 'reply_to_reply', post.content))
    return all_content


def find_posts_in_weeks(cur_user, all_posts_weekly, week_start, week_end, limit, write_to_file=False):
    weekly_data = all_posts_weekly[cur_user]
    cur_data = weekly_data[week_start:week_end]
    valid_posts = []
    for week in cur_data:
        for post in week:
            if len(post[2]) >= limit:
                valid_posts.append(post[2])
    print 'count valid posts', len(valid_posts)
    if write_to_file:
        with open('%s_week_%d_to_%d_posts.txt' %(cur_user,week_start, week_end), 'w') as outfile:
          outfile.write('\n----\n'.join(valid_posts).encode('utf-8').strip())
    return valid_posts


def count_modals(post):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(post)
    modal_count = 0
    verbs_count = 0
    for token in doc:
        if token.tag_.startswith('VB'):
            verbs_count += 1
        if token.tag_.startswith("MD"):
            modal_count += 1
    res = modal_count*1.0/(modal_count+verbs_count) if (modal_count+verbs_count)>0 else 0 
    return res

def count_total_children(post, func):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(post)
    children_counts = []
    for token in doc:
        children_counts.append(len([i for i in token.children]))
    children_counts = [i for i in children_counts if i != 0]
    return func(children_counts)


def analyse_users(write_user_post_info=False):
    all_users = User.query.find().all()
    all_posts_weekly = {}
    all_post_counts = {}
    earliest_date = datetime.datetime.strptime("2018-01-15 00:00:00", "%Y-%m-%d %H:%M:%S") # @Ri changed the cutoff time to match our data
    latest_date = datetime.datetime.strptime("2018-07-15 00:00:00", "%Y-%m-%d %H:%M:%S") # @Ri changed the cutoff time to match our data
    for user in all_users:
        posts = load_posts(user)
        if len(posts) < 1:
            continue
        week_start = earliest_date
        all_posts_weekly[user.username] = []
        while week_start < latest_date:
            week_end = week_start + datetime.timedelta(days=7)
            week_posts = [p for p in posts if (week_end > p[0] > week_start)]
            all_posts_weekly[user.username].append(week_posts)
            week_start = week_end

    if write_user_post_info:
        for user in all_users:
          if user.username not in all_posts_weekly:
              continue
          all_post_counts[user.username] = []
          for week in all_posts_weekly[user.username]:
              posts = [len(w[2]) for w in week]
              avg_len = np.mean(posts) if len(posts) > 0 else 0
              all_post_counts[user.username].append((len(week), avg_len))
        with open('user_stats.csv', 'w') as outfile:
          outfile.write('counts\n')
          for user in all_post_counts:
              outfile.write(user+'\t')
              counts = [str(w[0]) for w in all_post_counts[user]]
              outfile.write('\t'.join(counts))
              outfile.write('\n')
          outfile.write('avg length\n')
          for user in all_post_counts:
              outfile.write(user+'\t')
              lengths = [str(w[1]) for w in all_post_counts[user]]
              outfile.write('\t'.join(lengths))
              outfile.write('\n')
    return all_posts_weekly


def language_analysis():
    all_posts_weekly = analyse_users()
    cur_user = 'USERID_10_Username'
    early_posts = find_posts_in_weeks(cur_user, all_posts_weekly, 0, 2, 150)
    late_posts = find_posts_in_weeks(cur_user, all_posts_weekly, 14, 18, 150)
    methods = [np.mean, max, sum, len]
    for method in methods:
        print 'method: ', method
        early_scores = []
        
        for post in early_posts:
            early_scores.append(count_total_children(post, method))
        late_scores = []
        for post in late_posts:
            late_scores.append(count_total_children(post, method))
        print np.mean(early_scores)
        print np.mean(late_scores)

        print kruskal(early_scores, late_scores)

    print 'modals'
    early_scores = []
        
    for post in early_posts:
        early_scores.append(count_modals(post))
    late_scores = []
    for post in late_posts:
        late_scores.append(count_modals( post))
    print np.mean(early_scores)
    print np.mean(late_scores)
    print kruskal(early_scores, late_scores)


language_analysis()


