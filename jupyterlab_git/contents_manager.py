import os


class ContentsManagerWrapper:
    def __new__(cls, contents_manager):
        if hasattr(contents_manager, "jupytergit_os_path"):
            return super().__new__(JupyterGitAwareContentsManager)
        return super().__new__(cls)

    def __init__(self, contents_manager):
        self.contents_manager = contents_manager

    def jupytergit_os_path(self, path):
        return os.path.join(self.contents_manager.root_dir, path)

    @property
    def root_dir(self):
        return getattr(self.contents_manager, "root_dir", None)

    def get(self, *args, **kwargs):
        return self.contents_manager.get(*args, **kwargs)


class JupyterGitAwareContentsManager(ContentsManagerWrapper):
    def jupytergit_os_path(self, path):
        return self.contents_manager.jupytergit_os_path(path)
