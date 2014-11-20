file-compare-plugin
===================

Requirements:

1. If just a file type deployd and one host selected compare the repo files with the files on the host
2. If more than one host is selected comare files on the hosts against the first host in the list

__Note__: We need to address binary files 

Things to do:

1. Determine if a file.DeployedFile is different to what should be there, so different to a the file populated from the dictionary.
2. Compare a deployed file.DeployedFile from 2 different hosts.
3. Have live compare show the actual differences in the file, just like executing diff on them.
 
