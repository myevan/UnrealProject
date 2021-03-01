import unreal

def test_svn():
    import pb.tools.svn
    import uf.env
    import uf.contexts
    import uf.helpers

    import imp    
    imp.reload(pb.tools.svn)    
    imp.reload(uf.env)
    imp.reload(uf.contexts)
    imp.reload(uf.helpers)

    from uf.env import Environment
    from uf.contexts import SVNContext    
    svn_ctx = SVNContext.bind()
    svn_info = svn_ctx.get_info()

    env = Environment.get()
    assert(svn_info.path == env.project_dir_path)
    print(svn_info.url)
    print(svn_info.revision)

if __name__ == '__main__':
    test_svn()

