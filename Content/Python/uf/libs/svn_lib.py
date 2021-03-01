import unreal

from ..ctxs.svn_ctx import SVNContext

@unreal.uclass()
class SVNLibrary(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(params=[str], static=True, meta=dict(Category="PySubversion"))
    def bind_svn_dir(work_dir_path):
        return SVNContext.bind(work_dir_path)
    
    @unreal.ufunction(ret=bool, params=[], static=True, meta=dict(Category="PySubversion"))
    def load_svn_info():
        return SVNContext.get().load_info()

    @unreal.ufunction(ret=str, params=[], static=True, meta=dict(Category="PySubversion"))
    def get_svn_info_url():
        return SVNContext.get().get_info().url

    @unreal.ufunction(ret=int, params=[], static=True, meta=dict(Category="PySubversion"))
    def get_svn_info_revision():
        return SVNContext.get().get_info().revision