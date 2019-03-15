# This file is covered by the LICENSE file in the root of this project.
# @license <https://github.com/ArgLab/PiazzaDataAnalysisTool/LICENSE>
DataOutputDir=$1

SaveDir="$DataOutputDir/BarnesCourse/"
CurrDir=$(pwd)


for Collection in \
        piazza_content \
	piazza_content_changelog \
	piazza_content_history \
	piazza_content_children \
	piazza_content_children_history \
	piazza_content_children_subchildren \
	datasets \
	users \
	grade_data_final_grades \
	webassign_assignments \
	webassign_grades \
	webassign_questions \
	webassign_parts \
	webassign_partsubmissions \
	moodle_assignments \
	moodle_actions \
	tutorial_tutorials \
	tutorial_grades \
	tutorial_times \
	peertutor_transactions
do
    echo "Converting $Collection to csv"
    python json-to-csv.py "$SaveDir/$Collection.json" "$SaveDir/$Collection.csv"    
done