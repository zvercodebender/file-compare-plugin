from __future__ import with_statement
import sys
from overtherepy import OverthereHostSession, StringUtils

def remote_diff(session, source_file, remote_path):
    context.logOutput(remote_path)
    if source_file.isDirectory():
        t = session.work_dir_file("tmp")
    else:
        t = session.work_dir_file(source_file.name)
    session.copy_to(source_file, t)
    response = session.execute("diff %s %s" % (t.path, remote_path), check_success=False)
    return response.stdout
# End Def

#def local_diff(session, source_file, remote_path, sessionA, sessionB):
#    context.logOutput(remote_path)
#    local_fileA = "/somepath" . "/hostnameA/" . local_fileA
#    local_fileB = "/somepath" . "/hostnameB/" . local_fileB
#    sessionA.copy_to(remote_path, local_fileA)
#    sessionB.copy_to(remote_path, local_fileB)
#    response = execute("diff %s %s" % (local_fileA, local_fileB), check_success=False)
#    return response.stdout
# End Def

for d in thisCi.deployeds:
    dtype = str(d.deployable.type)
    if dtype == "file.File" or dtype == "file.Folder":
        if dtype == "file.File":
            print "%s/%s " % (d.targetPath, d.name)
            remote_path = "%s/%s" % (d.targetPath, d.name)
        else:
            print "%s/ " % (d.targetPath)
            remote_path = d.targetPath
        # End if
        with OverthereHostSession(d.container) as session:
            diff_lines = remote_diff(session, d.file, remote_path)
        if len(diff_lines) > 0:
            print "%s" % (diff_lines)
            context.logOutput(StringUtils.concat(diff_lines))
        # End if
    # End if  
# End for
