from __future__ import with_statement
import sys
import com.xebialabs.deployit.plugin.api.udm.Parameters
from overtherepy import OverthereHost, OverthereHostSession, Diff, StringUtils

def server_diff(hostA, hostB, source_file, remote_path):
    global OverthereHostSession
    global Diff

    context.logOutput(remote_path)
    sessionA = OverthereHostSession(hostA)
    sessionB = OverthereHostSession(hostB)
    try:
        print "Remote file %s" % (remote_path)
        d1 = sessionA.remote_file(remote_path)
        d2 = sessionB.remote_file(remote_path)
        print "Diff %s and %s" % (d1, d2)
        diff = Diff.calculate_diff(d1, d2)
        print str(diff.removed)
        print str(diff.added)
        print str(diff.changed)
    finally:
        sessionA.close_conn()
        sessionB.close_conn()
    # End try
    return response.stdout
# End Def

for d in thisCi.deployeds:
    dtype = str(d.deployable.type)
    if dtype == "file.File" or dtype == "file.Folder":
        if dtype == "file.File":
            #print "%s/%s " % (d.targetPath, d.name)
            remote_path = "%s/%s" % (d.targetPath, d.name)
        else:
            #print "%s/ " % (d.targetPath)
            remote_path = d.targetPath
        # End if
        targets = parameters["targets"]
        if len(targets) > 0 :
            hostA = targets.pop()
            hostB = targets.pop()
            diff_lines = server_diff(hostA, hostB, d.name, remote_path)
            if len(diff_lines) > 0:
                print "%s" % (diff_lines)
                context.logOutput(StringUtils.concat(diff_lines))
            # End if
        # End if
    # End if  
# End for
