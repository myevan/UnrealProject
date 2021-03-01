def test_svn():
    from pb.tools.svn_tool import SVNTool
    svn_tool = SVNTool()
    svn_info = svn_tool.get_info()
    assert(svn_info.path == '.')
    print(svn_info)

def test_log():
    from pb.log import LogHelper
    LogHelper.info("hello", name="World")

    from pb.loggers.json_logger import JsonLogger
    LogHelper.bind(JsonLogger())
    LogHelper.info("hello", name="JsonLogger", score=100)

def test_patterns():
    from pb.log import LogHelper
    from pb.patterns import singleton

    @singleton
    class Test:
        def __init__(self, name):
            self.name = name

        def hello(self):
            LogHelper.info("hello", name=self.name)

    t1 = Test("T1")
    t2 = Test("T2")
    t1.hello()
    t2.hello()

if __name__ == '__main__':
    if 0:
        test_svn()
    else:
        test_log()
        test_patterns()
