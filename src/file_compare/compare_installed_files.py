from __future__ import with_statement
import sys
import com.xebialabs.deployit.plugin.api.udm.Parameters
from overtherepy import OverthereHost, OverthereHostSession, LocalConnectionOptions, OperatingSystemFamily, StringUtils

def server_diff(hostA, hostB, source_file, remote_path):
    global LocalConnectionOptions
    global OverthereHostSession

    context.logOutput(remote_path)
    localOpts = LocalConnectionOptions(os=OperatingSystemFamily.UNIX)
    local_session =  OverthereHostSession(OverthereHost(localOpts))
    sessionA = OverthereHostSession(hostA)
    sessionB = OverthereHostSession(hostB)
    try:
        print "HostA = %s" % (hostA)
        print "d1 remote_file = %s" % (remote_path)
        d1 = sessionA.remote_file(remote_path)
        sfile = "hostA" + source_file
        local_d1 = local_session.work_dir_file(sfile)
        print "local_d1 work dir = %s" % (local_d1)
        print "copy %s to %s" % (d1, local_d1)
        local_session.copy_to(d1, local_d1, )

        print "HostB = %s" % (hostB)
        print "d2 remote_file = %s" % (remote_path)
        d2 = sessionB.remote_file(remote_path)
        sfile = "hostB" + source_file
        local_d2 = local_session.work_dir_file(sfile)
        print "local_d2 work dir = %s" % (local_d2)
        print "copy %s to %s" % (d2, local_d2)
        #local_session.copy_to(d2, local_d2)

        response = local_session.execute("diff %s %s" % (local_d1, local_d2), check_success=False)
    finally:
        sessionA.close_conn()
        sessionB.close_conn()
        local_session.close_conn()
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
