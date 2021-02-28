def test_svn():
    from pb.tools.svn import SVNManager
    svn_mgr = SVNManager()
    svn_info = svn_mgr.get_info()
    assert(svn_info.path == '.')
    print(svn_info)

if __name__ == '__main__':
    test_svn()

