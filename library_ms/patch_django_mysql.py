# 补丁文件：禁用Django的MySQL版本检查
import django.db.backends.base.base

# 检查方法是否存在，避免属性错误
def apply_patch():
    # 检查BaseDatabaseWrapper是否有check_database_version_supported方法
    if hasattr(django.db.backends.base.base.BaseDatabaseWrapper, 'check_database_version_supported'):
        # 保存原始方法
        original_check = django.db.backends.base.base.BaseDatabaseWrapper.check_database_version_supported
        
        # 重写方法以禁用版本检查
        def patched_check(self):
            # 跳过版本检查
            pass
        
        # 替换方法
        django.db.backends.base.base.BaseDatabaseWrapper.check_database_version_supported = patched_check

# 应用补丁
apply_patch()