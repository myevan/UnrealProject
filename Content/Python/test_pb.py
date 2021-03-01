def test_svn():
    from pb.tools.svn_tool import SVNTool
    svn_tool = SVNTool()
    svn_info = svn_tool.get_info()
    assert(svn_info.path == '.')
    print(svn_info)

def test_log():
    from pb import LogHelper
    LogHelper.info("hello", name="World")

    from pb.loggers.json_logger import JsonLogger
    LogHelper.bind(JsonLogger())
    LogHelper.info("hello", name="JsonLogger", score=100)

if __name__ == '__main__':
    test_log()
    #test_svn()
