# WoW Spell Database Editor (魔兽世界法术数据库编辑器)

这是一个用于编辑和管理 mangos 数据库中 spell_template 表的编辑器。

## 数据库连接信息
- 主机: 127.0.0.1
- 端口: 3306
- 用户名: root
- 密码: root
- 数据库: mangos
- 表名: spell_template

## 主要功能

1. 数据查询与编辑
   - 通过 Entry 和 Build 复合主键查询法术
   - 自动匹配最近的可用 Build 版本
   - 支持十六进制和十进制值的显示和编辑
   - 字段值修改历史记录

2. 界面布局
   - 左侧字段分类树
   - 中间数据编辑区域
   - 右侧字段说明面板
   - 字段分组显示
   - 支持字段过滤搜索

3. 数据对比
   - 支持不同 Entry 或 Build 之间的数据对比
   - 显示差异值
   - 保存对比历史记录
   - 可导出对比结果

4. 数据备份
   - 本地文件备份
   - JSON 格式存储
   - 支持备份恢复
   - 包含完整的字段映射

5. 快捷键支持
   - Ctrl+F: 聚焦搜索框
   - Ctrl+S: 保存更改
   - Ctrl+D: 数据对比

## 右键菜单功能

1. 值编辑
   - 复制/粘贴值
   - 设置为 0
   - 设置为 NULL

2. 字段操作
   - 查看字段说明
   - 查看修改历史
   - 恢复历史值

3. 数据操作
   - 备份当前数据
   - 恢复备份数据

## 使用说明

1. 查询数据
   - 输入法术 ID (Entry)
   - 输入或使用默认的 Build 版本 (5875)
   - 点击搜索或按回车键

2. 编辑数据
   - 直接在值列编辑
   - 支持十进制和十六进制输入
   - 自动格式化显示

3. 查看字段说明
   - 点击左侧分类树中的字段
   - 点击字段名
   - 右键字段名选择"查看字段说明"

4. 数据备份
   - 数据保存在 backups 目录
   - 文件名包含 Entry、Build 和时间戳
   - 可以随时恢复备份数据

## 注意事项

1. 数据验证
   - 自动验证数值范围
   - 保持数据类型一致性
   - 防止无效值输入

2. 备份建议
   - 重要修改前先备份
   - 定期备份重要数据
   - 保存备份到安全位置

3. 性能优化
   - 按需加载数据
   - 高效的数据缓存
   - 优化的查询性能 


## 备注
a. mpqpatcher.dll 是魔兽世界数据库编辑器 E:\VscodeProject\mpqpatcher\ConvToDll项目下面 

a.1.API 函数 check_listfile_str 用于检查 mpq 文件的完整性。
check_listfile_str = mpq_dll.check_listfile_str(mpq_file_path.encode('utf-8'))

a.2. API 函数 run_str 用于生成 MPQ 文件。sourcePath 是导入目录，导入目录下的所有文件, 而 mpqPath 是生成MPQ文件后的导出目录。
extern "C" __declspec(dllexport) int run_str(const char* mpqPath, const char* sourcePath) 

b
b.1 DBCGenerator.dll 是用于生成 DBC 文件的 DLL 库。 项目在E:\DBCGenerator 下面
        # 获取当前脚本所在目录的完整路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dll_path = os.path.join(current_dir, "DBCGenerator.dll")
        
        # 确保MySQL DLL可以被找到
        os.environ['PATH'] = current_dir + os.pathsep + os.environ['PATH']
        
        # 将DLL所在目录添加到系统路径
        os.add_dll_directory(current_dir)
        
        # 加载DLL
        mydll = ctypes.CDLL(dll_path)
        
        # 设置函数参数类型和返回值类型
        mydll.ExportDbcForDll.argtypes = [ctypes.c_char_p]
        mydll.ExportDbcForDll.restype = ctypes.c_int
        
        # 构建连接字符串
        connection_string = "127.0.0.1;3306;root;root;mangos"
        
        # 调用DLL函数
        result = mydll.ExportDbcForDll(connection_string.encode('utf-8'))
        
        if result == 1:
            print("DBC导出成功!")
        else:
            print("DBC导出失败!")

b.2 libmySQL.dll 是 MySQL 的 C API 库，用于连接和操作 MySQL 数据库。

以下是可以继续优化的功能列表：
数据编辑优化：
添加撤销/重做功能
添加批量替换功能
添加字段值的自动补全功能
添加字段值的有效性检查
界面优化：
添加深色/浅色主题切换
添加字体大小调整
添加表格列宽记忆功能
添加窗口布局保存功能
搜索功能增强：
添加模糊搜索功能
添加高级搜索（多条件组合）
添加搜索历史记录
添加相似法术推荐
数据分析功能：
添加字段值统计分析
添加数值范围分析
添加字段使用频率分析
添加数据可视化图表
导出功能增强：
添加自定义导出格式
添加导出模板管理
添加批量导出功能
添加导出预览功能
6. 配置管理：
添加数据库连接配置管理
添加用户偏好设置
添加快捷键自定义
添加工具栏自定义
性能优化：
添加数据缓存机制
优化大数据加载
优化内存使用
添加后台任务处理
辅助功能：
添加操作日志记录
添加数据校验工具
添加字段值计算器
添加常用值快捷输入