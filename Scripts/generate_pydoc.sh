# running this script will generate pydoc for ModSocDB and copy the html result into a
# folder named Documentation
# Each time it will remove the folder and generate it again to make sure old data is being
# replaced

 cd ../
 rm -rf ModSocDB/Documentation
 mkdir -p ModSocDB/Documentation
 pydoc -w ./ 
 mv *.html ModSocDB/Documentation/
 mv ModSocDB/Documentation .
