import os
import tornado
from .log import get_logger


class ContentsManagerWrapper:
    def __new__(cls, contents_manager):
        if hasattr(contents_manager, "jupytergit_os_path"):
            return super().__new__(JupyterGitAwareContentsManager)
        return super().__new__(cls)

    def __init__(self, contents_manager):
        self.contents_manager = contents_manager

    def jupytergit_os_path(self, path):
        return os.path.join(self.contents_manager.root_dir, path)

    def jupytergit_top_repo_os_path(self, path):
        return path

    def jupytergit_cm_path(self, path):
        return path

    @property
    def root_dir(self):
        return getattr(self.contents_manager, "root_dir", None)

    def get(self, *args, **kwargs):
        return self.contents_manager.get(*args, **kwargs)


class JupyterGitAwareContentsManager(ContentsManagerWrapper):
    def jupytergit_os_path(self, path):
        result_path = self.contents_manager.jupytergit_os_path(path)
        get_logger().debug(f"get os path '{path}' from jupytergit aware contents manager: {result_path}")
        if result_path is None:
            raise tornado.web.HTTPError(
                403, f"{path} can not contain a git repository"
            )
        return result_path

    def jupytergit_cm_path(self, os_path):
        result_path = self.contents_manager.jupytergit_cm_path(os_path)
        get_logger().debug(f"get cm path '{os_path}' from jupytergit aware contents manager: {result_path}")
        return result_path

    def jupytergit_top_repo_os_path(self, path):
        return self.jupytergit_os_path(path)
