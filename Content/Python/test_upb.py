import unreal

def test_svn():
    import pb.tools.svn
    import upb.env
    import upb.contexts
    import upb.helpers

    import imp    
    imp.reload(pb.tools.svn)    
    imp.reload(upb.env)
    imp.reload(upb.contexts)
    imp.reload(upb.helpers)

    from upb.env import Environment
    from upb.contexts import SVNContext    
    svn_ctx = SVNContext.bind()
    svn_info = svn_ctx.get_info()

    env = Environment.get()
    assert(svn_info.path == env.project_dir_path)
    print(svn_info.url)
    print(svn_info.revision)

if __name__ == '__main__':
    test_svn()

