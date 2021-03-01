import unreal

def test_svn():
    import pb.tools.svn_tool
    import uf.env
    import uf.ctxs.svn_ctx
    import uf.libs.svn_lib

    import imp    
    imp.reload(pb.tools.svn_tool)
    imp.reload(uf.env)
    imp.reload(uf.ctxs.svn_ctx)
    imp.reload(uf.libs.svn_lib)

    from uf.env import Environment
    from uf.ctxs.svn_ctx import SVNContext    
    svn_ctx = SVNContext.bind()
    svn_info = svn_ctx.get_info()

    env = Environment.get()
    assert(svn_info.path == env.project_dir_path)
    print(svn_info.url)
    print(svn_info.revision)

if __name__ == '__main__':
    test_svn()

