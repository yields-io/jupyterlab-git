import os


class ContentManagerWrapper:
    def __new__(cls, content_manager):
        if hasattr(content_manager, "jupytergit_os_path"):
            return super().__new__(JupyterGitAwareContentManager)
        return super().__new__(cls)

    def __init__(self, content_manager):
        self.content_manager = content_manager

    def jupytergit_os_path(self, path):
        return os.path.join(self.content_manager.root_dir, path)

    @property
    def root_dir(self):
        return getattr(self.contents_manager, "root_dir", None)

    def get(self, *args, **kwargs):
        return self.content_manager.get(*args, **kwargs)


class JupyterGitAwareContentManager(ContentManagerWrapper):
    def jupytergit_os_path(self, path):
        return self.content_manager.jupytergit_os_path(path)

    @property
    def root_dir(self):
        return None
