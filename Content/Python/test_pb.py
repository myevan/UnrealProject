def test_svn():
    from pb.tools.svn_tool import SVNTool
    svn_tool = SVNTool()
    svn_info = svn_tool.get_info()
    assert(svn_info.path == '.')
    print(svn_info)

if __name__ == '__main__':
    test_svn()

