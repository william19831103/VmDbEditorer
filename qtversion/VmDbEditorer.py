from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import mysql.connector
import os
import json
from datetime import datetime
import ctypes
import shutil
from PyQt5.QtWidgets import QDesktopWidget
import base64
import hashlib
from cryptography.fernet import Fernet
import time
from PyQt5.QtCore import QTranslator, QLocale

from licensing.models import *
from licensing.methods import Key, Helpers

# 更新授权信息
RSAPubKey = "<RSAKeyValue><Modulus>uQUWtKKob4exvz0nyAUF2uqqJKKrthzCDkHtiI1sZqvlUf6WUpN1WyCpIQlxGV8Bbc7ZpdqjeNoTa6wTtpAHPA2llOD2k5dZpxFH017RZdgBQQrZYO7rW8Bf0OcpuyY6I8E6PuCRNnuMsrp+NsSDtnzxI2mRgfimj148jD82PUhEQytRuN6t49B8LzGWNCP8Elp1m1RD2h6BLkImfEB4UF6V2qa9BxHUukYu6CjtgJrCxciHta7g18llAuYDIPDHlUkH+acBAMkYZXcld9gkSEY/Pj6BCbRQbL8cs84g4h/2WlFREcb4aKLbIqtng/RhnX1WDPzBmMYxm4H96EQEhw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI5ODU5MTAwMyIsIkFyeGVES1cvT0UvUXZuMFV2VDJZR2x0eDBub0cxTlVxTjFaeTh5enQiXQ=="


from spell_fields import (
    SPELL_FIELDS, 
    SPELL_ATTRIBUTES,
    SPELL_ATTRIBUTES_EX,
    SPELL_ATTRIBUTES_EX2,
    SPELL_ATTRIBUTES_EX3,
    SPELL_ATTRIBUTES_EX4,
    SPELL_STANCES,
    SPELL_TARGETS,
    SPELL_INTERRUPT_FLAGS,
    SPELL_AURA_INTERRUPT_FLAGS,
    SPELL_CHANNEL_INTERRUPT_FLAGS,
    parse_spell_flags,
    SPELL_EFFECTS,
    SPELL_EFFECT_MECHANICS,
    SPELL_AURA_TYPES,
    SPELL_SCHOOLS,
    SPELL_DAMAGE_CLASS,
    SPELL_POWER_TYPE,
    SPELL_FAMILY,
    SPELL_DISPEL_TYPE,
    SPELL_MECHANIC,
    SPELL_TARGET_CREATURE_TYPE,
    SPELL_PREVENTION_TYPE,
    SPELL_PROC_FLAGS,
    ITEM_CLASS,
    ITEM_SUBCLASS_WEAPON,
    ITEM_SUBCLASS_ARMOR,
    INVENTORY_TYPE,
    SPELL_RANGE,
    SPELL_DURATION,
    SPELL_CAST_TIME,
    SPELL_TARGET_TYPE,
    SPELL_AURA_STATE,
    SPELL_RADIUS,
    SPELL_EFFECT_TARGET,
    SPELL_IMPLICIT_TARGETS,
    SPELL_CUSTOM_FLAGS,
)
from config import Config
from logger import logger

# 在类的开始处添加字段分类定义
FIELD_CATEGORIES = {
    '基本信息': ['entry', 'build', 'school', 'category', 'castUI', 'dispel', 'mechanic'],
    '属性标志': ['attributes', 'attributesEx', 'attributesEx2', 'attributesEx3', 'attributesEx4'],
    '目标设置': ['targets', 'targetCreatureType', 'requiresSpellFocus', 'casterAuraState', 'targetAuraState'],
    '施法相关': ['castingTimeIndex', 'recoveryTime', 'categoryRecoveryTime', 'interruptFlags', 'auraInterruptFlags', 'channelInterruptFlags'],
    '触发设置': ['procFlags', 'procChance', 'procCharges'],
    '等级相关': ['maxLevel', 'baseLevel', 'spellLevel'],
    '法力消耗': ['powerType', 'manaCost', 'manCostPerLevel', 'manaPerSecond', 'manaPerSecondPerLevel'],
    '效果1': ['effect1', 'effectDieSides1', 'effectBaseDice1', 'effectDicePerLevel1', 'effectRealPointsPerLevel1', 'effectBasePoints1', 'effectMechanic1'],
    '效果2': ['effect2', 'effectDieSides2', 'effectBaseDice2', 'effectDicePerLevel2', 'effectRealPointsPerLevel2', 'effectBasePoints2', 'effectMechanic2'],
    '效果3': ['effect3', 'effectDieSides3', 'effectBaseDice3', 'effectDicePerLevel3', 'effectRealPointsPerLevel3', 'effectBasePoints3', 'effectMechanic3'],
    '视觉效果': ['spellVisual1', 'spellVisual2', 'spellIconId', 'activeIconId'],
    '文本相关': ['name', 'nameFlags', 'nameSubtext', 'description', 'auraDescription'],
    '其他设置': ['spellFamilyName', 'spellFamilyFlags', 'dmgClass', 'preventionType', 'customFlags']
}

class SpellDatabaseEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口图标
        icon = QIcon("app.ico")
        self.setWindowIcon(icon)
        # 设置任务栏图标
        if os.name == 'nt':  # Windows系统
            import ctypes
            myappid = 'mycompany.spelldbeditor.1.0'  # 任意字符串
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        self.current_entry = None
        self.current_build = None
        self.compare_history = []
        self.max_history = 10
        self.field_history = {}
        self.max_field_history = 10
        
        # 添加撤销/重做栈
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo = 50
        
        # 添加字段值历史记录
        self.field_value_history = {}
        
        # 加载配置
        self.config = Config()
        
        # 初始化UI
        self.initUI()
        
        # 应用用户偏好设置
        self.applyPreferences()
        
        # 恢复窗口布局
        self.restoreLayout()
        
        # 设置快捷键
        self.setupShortcuts()
        
        # 恢复窗口位置和大小
        self.restoreWindowState()
        
        # 最后尝试初始化数据库连接
        try:
            self.initDatabase()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'数据库连接失败: {str(e)}')
            self.statusBar().showMessage('数据库连接失败')

    def setupShortcuts(self):
        """设置快捷键"""
        # 搜索 - Ctrl+F
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(self.focusSearch)
        
        # 保存 - Ctrl+S
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.saveChanges)
        
        # 导出 - Ctrl+E
        export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_shortcut.activated.connect(self.exportData)
        
        # 数据对比 - Ctrl+D
        compare_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        compare_shortcut.activated.connect(self.compareData)
        
        # 添加撤销/重做快捷键
        undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_shortcut.activated.connect(self.undo)
        
        redo_shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)
        redo_shortcut.activated.connect(self.redo)

    def focusSearch(self):
        """聚焦到搜索框"""
        self.search_entry.setFocus()
        self.search_entry.selectAll()  # 中所有文本，方便直接输入
    
    def initUI(self):
        self.setWindowTitle('魔兽世界法术数据库编辑器')
        self.setGeometry(100, 100, 1920, 1000)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 工具栏区域
        toolbar_layout = QHBoxLayout()
        
        # 搜索区域
        search_layout = QHBoxLayout()
        
        # Entry输入框
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('输入法术ID(entry)')
        self.search_entry.returnPressed.connect(self.searchSpell)
        
        # Build输入框
        self.search_build = QLineEdit('5875')  # 默认值5875
        self.search_build.setPlaceholderText('构建版本(build)')
        self.search_build.returnPressed.connect(self.searchSpell)
        
        search_button = QPushButton('搜索')
        search_button.clicked.connect(self.searchSpell)
        
        # 在搜索按钮后添加高级搜索按钮
        advanced_search_button = QPushButton('高级搜索')
        advanced_search_button.clicked.connect(self.showAdvancedSearch)
        search_layout.addWidget(advanced_search_button)
        
        search_layout.addWidget(QLabel('Entry:'))
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(QLabel('Build:'))
        search_layout.addWidget(self.search_build)
        search_layout.addWidget(search_button)
        
        # 字段过滤
        self.field_filter = QLineEdit()
        self.field_filter.setPlaceholderText('过滤字段名...')
        self.field_filter.textChanged.connect(self.filterFields)
        search_layout.addWidget(QLabel('字段过滤:'))
        search_layout.addWidget(self.field_filter)
        
        toolbar_layout.addLayout(search_layout)
        toolbar_layout.addStretch()
        
        # 添加保存按钮
        save_button = QPushButton('保存更改')
        save_button.clicked.connect(self.saveChanges)
        toolbar_layout.addWidget(save_button)
        
        # 添加数据对比按钮
        compare_button = QPushButton('数据对')
        compare_button.clicked.connect(self.compareData)
        toolbar_layout.addWidget(compare_button)
        
        # 添加复制法术按钮
        copy_spell_button = QPushButton('复制法术')
        copy_spell_button.clicked.connect(self.copySpell)
        toolbar_layout.addWidget(copy_spell_button)
        
        # 在工具栏添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)  # 垂直线
        separator.setFrameShadow(QFrame.Sunken)  # 下沉效果
        separator.setFixedWidth(2)  # 设置宽度
        toolbar_layout.addWidget(separator)
        
        # 添加备份按钮
        backup_button = QPushButton('备份数据')
        backup_button.setToolTip('备份当前法术数据')
        backup_button.clicked.connect(self.backupData)
        toolbar_layout.addWidget(backup_button)
        
        # 添加恢复按钮
        restore_button = QPushButton('恢复备份')
        restore_button.setToolTip('恢复之前的备份数')
        restore_button.clicked.connect(self.restoreBackup)
        toolbar_layout.addWidget(restore_button)
        
        # 添加生成DBC按钮
        generate_dbc_button = QPushButton('生成SPELL.DBC')
        generate_dbc_button.setToolTip('生成SPELL.DBC文件')
        generate_dbc_button.clicked.connect(self.generateSpellDBC)
        toolbar_layout.addWidget(generate_dbc_button)
        
        # 添加生成MPQ按钮 
        generate_mpq_button = QPushButton('生成MPQ')
        generate_mpq_button.setToolTip('生成MPQ文件')
        generate_mpq_button.clicked.connect(self.generateMPQ)
        toolbar_layout.addWidget(generate_mpq_button)
        
        # 加配置按钮
        config_button = QPushButton('配置管理')
        config_button.clicked.connect(self.showConfigDialog)
        toolbar_layout.addWidget(config_button)
        
        main_layout.addLayout(toolbar_layout)
        
        # 创建主分割器
        main_splitter = QSplitter(Qt.Horizontal)
        
        # 添加分类树
        category_tree = self.initCategoryView()
        main_splitter.addWidget(category_tree)
        
        # 创建侧内容区域
        content_splitter = QSplitter(Qt.Horizontal)
        
        # 表格区域
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        self.table = QTableWidget()
        self.table.itemChanged.connect(self.onItemChanged)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showContextMenu)
        table_layout.addWidget(self.table)
        
        # 说面板
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        self.field_name_label = QLabel('字段说明')
        self.field_name_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                padding: 5px;
                background: #f0f0f0;
                border-bottom: 1px solid #ccc;
            }
        """)
        info_layout.addWidget(self.field_name_label)
        self.info_text = QTextBrowser()
        info_layout.addWidget(self.info_text)
        
        # 添加到右侧分割器
        content_splitter.addWidget(table_widget)
        content_splitter.addWidget(info_widget)
        content_splitter.setStretchFactor(0, 2)
        content_splitter.setStretchFactor(1, 1)
        
        # 添加到主分割器
        main_splitter.addWidget(content_splitter)
        
        # 设置分割器比例
        main_splitter.setStretchFactor(0, 1)  # 分类树
        main_splitter.setStretchFactor(1, 4)  # 内容区域
        
        # 添加到主布局
        main_layout.addWidget(main_splitter)
        
        # 初始化表格
        self.initTable()
        
        # 添加状态栏
        self.statusBar().showMessage('就绪')
        
    def onItemChanged(self, item):
        if not self.isVisible():
            return
        
        if item.column() % 2 == 1:  # 值列
            row = item.row()
            col = item.column()
            field_col = col - 1
            
            field_item = self.table.item(row, field_col)
            if field_item:
                field_name = field_item.text()
                new_value = item.text().strip()
                
                # 获取修改前的值
                old_value = getattr(item, '_old_value', item.text())
                
                if not new_value:
                    return
                
                # 验证和格式化值
                valid, formatted_value = self.validateAndFormatValue(field_name, new_value)
                
                if valid:
                    if formatted_value != old_value:
                        # 添加撤销动作
                        self.addUndoAction(field_name, old_value, formatted_value, row, col)
                        
                        # 添加到修改历史
                        self.addFieldHistory(field_name, old_value, formatted_value)
                        
                        # 更新显示
                        self.table.blockSignals(True)
                        item.setText(formatted_value)
                        # 保存当前值作为下次修改的旧值
                        item._old_value = formatted_value
                        self.table.blockSignals(False)
                        
                        # 更新自动补全历史
                        if field_name in self.field_value_history:
                            if formatted_value not in self.field_value_history[field_name]:
                                self.field_value_history[field_name].append(formatted_value)
                        
                        self.statusBar().showMessage(f'字段 {field_name} 已修改为: {formatted_value}')
                else:
                    QMessageBox.warning(self, '警告', f'无效的值: {formatted_value}')
                    self.restoreValue(row, col)
    
    def restoreValue(self, row, col):
        """恢复单元格的原始值"""
        if not self.current_entry:
            return
        
        try:
            # 获取段名
            field_col = col - 1
            field_item = self.table.item(row, field_col)
            if not field_item:
                return
            
            field_name = field_item.text()
            
            # 查询原始值
            self.cursor.execute(f"SELECT {field_name} FROM spell_template WHERE entry = %s", (self.current_entry,))
            result = self.cursor.fetchone()
            
            if result and result[0] is not None:
                value = result[0]
                field_type = SPELL_FIELDS[field_name]
                
                # 格式值
                if field_type in ['int', 'bigint', 'smallint']:
                    formatted_value = f"{int(value)} (0x{int(value):X})"
                else:
                    formatted_value = str(value)
                    
                # 更新单元格
                value_item = self.table.item(row, col)
                if value_item:
                    value_item.setText(formatted_value)
                    
        except Exception as e:
            print(f"恢复值失���������: {str(e)}")
    
    def saveChanges(self):
        if not self.current_entry or not hasattr(self, 'current_build'):
            QMessageBox.warning(self, '警告', '没有加载的法术数据')
            return
        
        try:
            # 先获取当前数据库中的数据
            self.cursor.execute(
                "SELECT * FROM spell_template WHERE entry = %s AND build = %s",
                (self.current_entry, self.current_build)
            )
            current_data = self.cursor.fetchone()
            
            if not current_data:
                QMessageBox.warning(self, '警告', '数据已不存在')
                return
            
            # 获取列名
            self.cursor.execute("SHOW COLUMNS FROM spell_template")
            columns = [column[0] for column in self.cursor.fetchall()]
            current_data_dict = dict(zip(columns, current_data))
            
            # 收集修改的数据
            updates = []
            params = []
            rows = self.table.rowCount()
            
            for col in range(0, self.table.columnCount(), 2):
                for row in range(rows):
                    field_item = self.table.item(row, col)
                    value_item = self.table.item(row, col + 1)
                    
                    if field_item and value_item and value_item.text():
                        field_name = field_item.text()
                        value_text = value_item.text()
                        
                        # 检查字段类型并转换值
                        field_type = SPELL_FIELDS.get(field_name)
                        if field_type in ['int', 'bigint', 'smallint']:
                            try:
                                # 提取数值部分（去除十六进制显示）
                                value = int(value_text.split('(')[0].strip())
                            except:
                                continue
                        else:
                            value = value_text
                        
                        # 只有当生变化时才更新
                        if field_name in current_data_dict and str(current_data_dict[field_name]) != str(value):
                            updates.append(f"{field_name} = %s")
                            params.append(value)
            
            if updates:
                # 使用复合主键更新
                query = f"UPDATE spell_template SET {', '.join(updates)} WHERE entry = %s AND build = %s"
                params.extend([self.current_entry, self.current_build])
                
                self.cursor.execute(query, params)
                self.conn.commit()
                
                QMessageBox.information(self, '成功', '数据已保存')
                self.statusBar().showMessage('数据已保存')
                
                # 重新加载数据
                self.searchSpell()
            else:
                self.statusBar().showMessage('没有数据需要更新')
        
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保存失败: {str(e)}')
            self.conn.rollback()
    
    def exportData(self):
        if not self.current_entry:
            QMessageBox.warning(self, '警告', '没有加载的法术数据')
            return
            
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "导出据",
                f"spell_{self.current_entry}.csv",
                "CSV Files (*.csv)"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    # 写入表头
                    headers = []
                    for col in range(0, self.table.columnCount(), 2):
                        headers.append("字段名,值")
                    f.write(','.join(headers) + '\n')
                    
                    # 写入数据
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            if item:
                                row_data.append(f'"{item.text()}"')
                            else:
                                row_data.append('""')
                        f.write(','.join(row_data) + '\n')
                        
                QMessageBox.information(self, '成功', f'数据已导出到: {filename}')
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'导出失败: {str(e)}')
    
    def filterFields(self, text):
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(0, self.table.columnCount(), 2):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
    
    def searchSpell(self):
        """查询法术数据"""
        # 如果窗口还未显示，忽略调用
        if not self.isVisible():
            return
        
        # 检查数据库连接
        if not hasattr(self, 'conn') or not self.conn or not self.conn.is_connected():
            try:
                if not self.initDatabase():
                    QMessageBox.critical(self, '错误', '无法连接到数据库')
                    return
            except Exception as e:
                QMessageBox.critical(self, '错误', f'数据库连接失败: {str(e)}')
                return
        
        entry = self.search_entry.text().strip()
        build = self.search_build.text().strip()
        
        # 验证entry
        if not entry:
            QMessageBox.warning(self, '警告', '请输入法术ID')
            return
        
        # 验证build
        if not build:
            build = '5875'  # 默认值
            self.search_build.setText(build)
        
        # 验证输入是否为数字
        try:
            entry = int(entry)
            build = int(build)
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的数值')
            return
        
        try:
            # 先获取该entry的有可用build
            self.cursor.execute(
                "SELECT DISTINCT build FROM spell_template WHERE entry = %s ORDER BY build DESC",
                (entry,)
            )
            available_builds = [row[0] for row in self.cursor.fetchall()]
            
            if not available_builds:
                QMessageBox.information(self, '提示', f'未找到法术ID: {entry}的任何版本')
                return
            
            # 找到最接近且不大于指定build的值
            target_build = None
            for b in available_builds:
                if b <= build:
                    target_build = b
                    break
            
            # 如果没找到小于等于指定build的值，使用最小的build
            if target_build is None:
                target_build = min(available_builds)
            
            # 如果实际使用的build与输不同，更新输入框
            if target_build != build:
                self.search_build.setText(str(target_build))
                self.statusBar().showMessage(f'已自动选择最接近的Build版本: {target_build}')
            
            # 使用确定的build询数据
            # 先获取列名
            self.cursor.execute("SHOW COLUMNS FROM spell_template")
            columns = [column[0] for column in self.cursor.fetchall()]
            
            # 查询数据
            self.cursor.execute(
                "SELECT * FROM spell_template WHERE entry = %s AND build = %s",
                (entry, target_build)
            )
            result = self.cursor.fetchone()
            
            if result:
                self.current_entry = entry
                self.current_build = target_build
                
                # 阻止表格信号
                self.table.blockSignals(True)
                
                # 创建字段名到值的映射
                data_dict = dict(zip(columns, result))
                
                # 更新表格数据
                rows = self.table.rowCount()
                field_names = list(SPELL_FIELDS.keys())
                
                for field_idx, field_name in enumerate(field_names):
                    if field_name in data_dict:
                        value = data_dict[field_name]
                        
                        # 计算位置
                        col = (field_idx // rows) * 2
                        row = field_idx % rows
                        
                        # 格式化值
                        if value is not None:
                            field_type = SPELL_FIELDS[field_name]
                            if field_type in ['int', 'bigint', 'smallint']:
                                try:
                                    field_value = f"{int(value)} (0x{int(value):X})"
                                except:
                                    field_value = str(value)
                            else:
                                field_value = str(value)
                        else:
                            field_value = ''
                        
                        # 设置值
                        value_item = self.table.item(row, col + 1)
                        if value_item:
                            value_item.setText(field_value)
                
                # 恢复表格信号
                self.table.blockSignals(False)
                
                self.statusBar().showMessage(f'已加载法术ID: {entry}, Build: {target_build}')
            else:
                QMessageBox.information(self, '提示', f'未找到法ID: {entry}, Build: {target_build}')
                
        except mysql.connector.Error as e:
            QMessageBox.critical(self, '错误', f'数据库询失败: {str(e)}')
            self.statusBar().showMessage('查询失败')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'查询失败: {str(e)}')
            self.statusBar().showMessage('查询失败')
    
    def initDatabase(self):
        """初始化数据库连接"""
        try:
            db_config = self.config.get_database_config()
            # 添加auth_plugin配置
            db_config['auth_plugin'] = 'mysql_native_password'
            # 添加 use_pure 参数
            db_config['use_pure'] = True
            
            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor(buffered=True)
            self.statusBar().showMessage('数据库连接成功')
            return True
        except Exception as e:
            self.conn = None
            self.cursor = None
            # 显示详细的错误信息
            error_msg = f'数据库连接失败: {str(e)}\n'
            error_msg += f'配置信息: {db_config}\n'
            error_msg += '请检查:\n1. 数据库服务是否启动\n2. 配置信息是否正确\n3. 网络连接是否正常'
            QMessageBox.critical(self, '错误', error_msg)
            raise e
    
    def initTable(self):
        # 设置列数为4
        COLUMNS = 4
        total_fields = len(SPELL_FIELDS)
        rows = (total_fields + COLUMNS - 1) // COLUMNS
        
        # 设置表格的行列数
        self.table.setRowCount(rows)
        self.table.setColumnCount(COLUMNS * 2)  # 每组需要2列(字段名和值)
        
        # 设置表头
        headers = []
        for i in range(COLUMNS):
            headers.extend([f'字段名_{i+1}', f'值_{i+1}'])
        self.table.setHorizontalHeaderLabels(headers)
        
        # 填充字段
        field_names = list(SPELL_FIELDS.keys())
        for field_idx, field_name in enumerate(field_names):
            # 计算行列位置
            col = (field_idx // rows) * 2  # 每组占用2列
            row = field_idx % rows
            
            # 加字段名
            name_item = QTableWidgetItem(field_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # 字段名不可编辑
            self.table.setItem(row, col, name_item)
            
            # 添加值单元格
            value_item = QTableWidgetItem('')
            # 禁用值单元格的回车键编辑完成功能
            value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
            value_item.setFlags(value_item.flags() | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.table.setItem(row, col + 1, value_item)
        
        # 设置列宽
        for i in range(COLUMNS):
            self.table.setColumnWidth(i * 2, 150)     # 字段名列
            self.table.setColumnWidth(i * 2 + 1, 200) # 值列
            
        # 设置表格属性
        self.table.setAlternatingRowColors(True)  # 交替行颜色
        self.table.verticalHeader().setVisible(False)  # 隐藏行号
        
        # 设置表格的选择模式
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        
        # 设置表格样式
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f6f6f6;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        
        # 设置表头样式
        header = self.table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
        """)
        
        # 设工具提示显示延迟
        self.table.setToolTipDuration(5000)  # 5秒
        
        # 添加字段名单元格的点击事件
        self.table.itemClicked.connect(self.onTableItemClicked)
        
        # 只保留点击事件
        # self.table.setMouseTracking(True)
        # self.table.cellEntered.connect(self.onCellEntered)
    
    def onTableItemClicked(self, item):
        """处理表格单元格点击事件"""
        row = item.row()
        col = item.column()
        
        # 获取字段名（无论点击的是字段名还是值）
        field_col = col - 1 if col % 2 == 1 else col
        field_item = self.table.item(row, field_col)
        
        if field_item:
            field_name = field_item.text()
            # 如果点击的是值列，同时获值
            if col % 2 == 1:
                value = item.text()
                self.showFieldInfo(field_name, value)
            else:
                self.showFieldInfo(field_name)
    
    def showContextMenu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 获取当选中的单元
        item = self.table.itemAt(pos)
        if item:
            row = item.row()
            col = item.column()
            
            # 复制值
            copy_action = menu.addAction('复制')
            copy_action.triggered.connect(lambda: self.copyValue(item))
            
            # 如果是值列，添加编辑选项
            if col % 2 == 1:
                # 粘贴值
                paste_action = menu.addAction('粘值')
                paste_action.triggered.connect(lambda: self.pasteValue(item))
                
                menu.addSeparator()
                
                # 设为0
                zero_action = menu.addAction('设为0')
                zero_action.triggered.connect(lambda: self.setValueToZero(item))
                
                # 设为null
                null_action = menu.addAction('设为NULL')
                null_action.triggered.connect(lambda: self.setValueToNull(item))
            
            # 如果是字段名列，添加查看说明选项
            if col % 2 == 0:
                menu.addSeparator()
                info_action = menu.addAction('查看字段说明')
                info_action.triggered.connect(lambda: self.showFieldInfo(item.text()))
                
                # 添加历史记录选
                history_action = menu.addAction('查看修改历史')
                history_action.triggered.connect(lambda: self.showFieldHistory(item.text()))
            
            menu.addSeparator()
            
            # 添加备份选项
            backup_action = menu.addAction('备份当前数据')
            backup_action.triggered.connect(self.backupData)
            
            # 添加恢复选项
            restore_action = menu.addAction('恢复备份数据')
            restore_action.triggered.connect(self.restoreBackup)
        
        menu.exec_(self.table.viewport().mapToGlobal(pos))
    
    def copyValue(self, item):
        """���制单元格值到剪贴板"""
        QApplication.clipboard().setText(item.text())
    
    def pasteValue(self, item):
        """从剪贴板粘贴值"""
        text = QApplication.clipboard().text()
        item.setText(text)
    
    def setValueToZero(self, item):
        """设置值为0"""
        item.setText('0 (0x0)')
    
    def setValueToNull(self, item):
        """设置值为NULL"""
        item.setText('')
    
    def showFieldInfo(self, field_name, value=None):
        """显示段说明"""
        # 更新字名标签
        field_desc = {
            'entry': '法术ID',
            'build': '客户端版本号',
            'school': '法术学派',
            'category': '法术分类',
            'castUI': '施法界面',
            'dispel': '驱散类型',
            'mechanic': '机制类型',
            'attributes': '属性标志',
            'attributesEx': '扩展属性标志1',
            'attributesEx2': '扩展属性标志2',
            'attributesEx3': '扩展属性标志3',
            'attributesEx4': '扩展属性标志4',
            'stances': '可用姿态',
            'stancesNot': '不可用姿态',
            'targets': '目标标志',
            'targetCreatureType': '目标生物类型',
            'requiresSpellFocus': '需要法术焦点',
            'casterAuraState': '施法者光环状态',
            'targetAuraState': '目标光环状态',
            'castingTimeIndex': '施法时间索引',
            'recoveryTime': '恢复时间',
            'categoryRecoveryTime': '分类恢复时间',
            'interruptFlags': '打断标志',
            'auraInterruptFlags': '光环打断标志',
            'channelInterruptFlags': '引导打断标志',
            'procFlags': '触发标志',
            'procChance': '触发几率',
            'procCharges': '触发次数',
            'maxLevel': '最高等级',
            'baseLevel': '基础等级',
            'spellLevel': '法术等级',
            'durationIndex': '持续时间索引',
            'powerType': '能量类型',
            'manaCost': '法力消耗',
            'manaCostPerLevel': '每级法力消耗',
            'manaPerSecond': '每秒法力消耗',
            'manaPerSecondPerLevel': '每级每秒法力消耗',
            'rangeIndex': '范围索引',
            'speed': '法术速度',
            'modelNextSpell': '下一个法术模型',
            'stackAmount': '堆叠数量',
            'totem1': '图腾1',
            'totem2': '图腾2',
            'reagent1': '材料1',
            'reagent2': '材料2',
            'reagent3': '材料3',
            'reagent4': '材料4',
            'reagent5': '材料5',
            'reagent6': '材料6',
            'reagent7': '材料7',
            'reagent8': '材料8',
            'reagentCount1': '材料1数量',
            'reagentCount2': '材料2数量',
            'reagentCount3': '材料3数量',
            'reagentCount4': '材料4数量',
            'reagentCount5': '材料5数量',
            'reagentCount6': '材料6数量',
            'reagentCount7': '材料7数量',
            'reagentCount8': '材料8数量',
            'equippedItemClass': '需要装备类型',
            'equippedItemSubClassMask': '需要装备子类型掩码',
            'equippedItemInventoryTypeMask': '需要装备栏位掩码',
            'effect1': '效果1',
            'effect2': '效果2',
            'effect3': '效果3',
            'effectDieSides1': '效果1骰子面数',
            'effectDieSides2': '效果2骰子面数',
            'effectDieSides3': '效果3骰子面数',
            'effectBaseDice1': '效果1基础骰子数',
            'effectBaseDice2': '效果2基础骰子数',
            'effectBaseDice3': '效果3基础骰子数',
            'effectDicePerLevel1': '效果1每级骰子数',
            'effectDicePerLevel2': '效果2每级骰子数',
            'effectDicePerLevel3': '效果3每级骰子数',
            'effectRealPointsPerLevel1': '效果1每级实际点数',
            'effectRealPointsPerLevel2': '效果2每级实际点数',
            'effectRealPointsPerLevel3': '效果3每级实际点数',
            'effectBasePoints1': '效1基础点数',
            'effectBasePoints2': '效果2基础点数',
            'effectBasePoints3': '效果3基础点数',
            'effectMechanic1': '效果1机制',
            'effectMechanic2': '效果2机制',
            'effectMechanic3': '效果3机制',
            'effectImplicitTargetA1': '效果1隐含目标A',
            'effectImplicitTargetA2': '效果2隐含目标A',
            'effectImplicitTargetA3': '效果3隐含目标A',
            'effectImplicitTargetB1': '效果1隐含目标B',
            'effectImplicitTargetB2': '效果2隐含目标B',
            'effectImplicitTargetB3': '效果3隐含目标B',
            'effectRadiusIndex1': '效果1半径索引',
            'effectRadiusIndex2': '效果2半径索引',
            'effectRadiusIndex3': '效果3半径索引',
            'effectApplyAuraName1': '效果1光环名称',
            'effectApplyAuraName2': '效果2光环名称',
            'effectApplyAuraName3': '效果3光环名称',
            'effectAmplitude1': '效果1周期',
            'effectAmplitude2': '效果2周期',
            'effectAmplitude3': '效果3周期',
            'effectMultipleValue1': '效果1倍数值',
            'effectMultipleValue2': '效果2倍数值',
            'effectMultipleValue3': '效果3倍数值',
            'effectChainTarget1': '效果1连锁目标数',
            'effectChainTarget2': '效果2连锁目标数',
            'effectChainTarget3': '效果3连锁目标数',
            'effectItemType1': '效果1物品类型',
            'effectItemType2': '效果2物品类型',
            'effectItemType3': '效果3物品类型',
            'effectMiscValue1': '效果1杂项值',
            'effectMiscValue2': '效果2杂项值',
            'effectMiscValue3': '效果3杂项值',
            'effectTriggerSpell1': '效果1��发法术',
            'effectTriggerSpell2': '效果2触发法术',
            'effectTriggerSpell3': '效果3触发法术',
            'effectPointsPerComboPoint1': '效果1每连击点数值',
            'effectPointsPerComboPoint2': '效果2每连击点数值',
            'effectPointsPerComboPoint3': '效果3每连击点数值',
            'spellVisual1': '法术视觉效果1',
            'spellVisual2': '法术视觉效果2',
            'spellIconId': '法术图标ID',
            'activeIconId': '激活图标ID',
            'spellPriority': '法术优先级',
            'name': '法术名称',
            'nameFlags': '名称标志',
            'nameSubtext': '名称子文本',
            'nameSubtextFlags': '名称子文本标志',
            'description': '法术描述',
            'descriptionFlags': '描述标志',
            'auraDescription': '光环描述',
            'auraDescriptionFlags': '光环描述标志',
            'manaCostPercentage': '法力消耗百分比',
            'startRecoveryCategory': '开始恢复分类',
            'startRecoveryTime': '开始恢复时间',
            'minTargetLevel': '最低目标等级',
            'maxTargetLevel': '最高目标等级',
            'spellFamilyName': '法术族名称',
            'spellFamilyFlags': '法术族标志',
            'maxAffectedTargets': '最大影响目标数',
            'dmgClass': '伤害类型',
            'preventionType': '防护类型',
            'stanceBarOrder': '姿态条顺序',
            'dmgMultiplier1': '伤害倍数1',
            'dmgMultiplier2': '伤害倍数2',
            'dmgMultiplier3': '伤害倍数3',
            'minFactionId': '最低阵营ID',
            'minReputation': '最低声望',
            'requiredAuraVision': '需要光环视觉',
            'customFlags': '自定义标志'
        }

        # 获取字段的中文说明
        field_description = field_desc.get(field_name, field_name)
        self.field_name_label.setText(f'字段: {field_name} ({field_description})')
        
        try:
            # 将字段分为两类处理
            bit_flag_fields = [
                'attributes', 'attributesEx', 'attributesEx2', 'attributesEx3', 'attributesEx4',
                'stances', 'stancesNot', 'targets', 'interruptFlags', 
                'auraInterruptFlags', 'channelInterruptFlags', 'procFlags',
                'effectTargetFlags1', 'effectTargetFlags2', 'effectTargetFlags3',
                'customFlags'
            ]
            
            enum_fields = [
                'effect1', 'effect2', 'effect3',
                'effectMechanic1', 'effectMechanic2', 'effectMechanic3',
                'effectApplyAuraName1', 'effectApplyAuraName2', 'effectApplyAuraName3',
                'school', 'dmgClass', 'powerType', 'spellFamilyName', 'dispel', 
                'mechanic', 'targetCreatureType', 'preventionType',
                'rangeIndex', 'durationIndex', 'castingTimeIndex',  # 添加新字段
                'targetAuraState', 'casterAuraState',
                'effectRadiusIndex1', 'effectRadiusIndex2', 'effectRadiusIndex3',
                'effectImplicitTargetA1', 'effectImplicitTargetA2', 'effectImplicitTargetA3',
                'effectImplicitTargetB1', 'effectImplicitTargetB2', 'effectImplicitTargetB3',
            ]
            
            if field_name in bit_flag_fields + enum_fields and value:
                # 将值转换为整数
                if isinstance(value, str):
                    if '(' in value and '0x' in value:
                        value = int(value.split('(')[0].strip())
                    elif '0x' in value.lower():
                        value = int(value.replace('0x', ''), 16)
                    else:
                        value = int(value)
                
                # 获取对应的字典
                flag_dict = {
                    'attributes': SPELL_ATTRIBUTES,
                    'attributesEx': SPELL_ATTRIBUTES_EX,
                    'attributesEx2': SPELL_ATTRIBUTES_EX2,
                    'attributesEx3': SPELL_ATTRIBUTES_EX3,
                    'attributesEx4': SPELL_ATTRIBUTES_EX4,
                    'stances': SPELL_STANCES,
                    'stancesNot': SPELL_STANCES,
                    'targets': SPELL_TARGETS,
                    'interruptFlags': SPELL_INTERRUPT_FLAGS,
                    'auraInterruptFlags': SPELL_AURA_INTERRUPT_FLAGS,
                    'channelInterruptFlags': SPELL_CHANNEL_INTERRUPT_FLAGS,
                    'procFlags': SPELL_PROC_FLAGS,
                    'effect1': SPELL_EFFECTS,
                    'effect2': SPELL_EFFECTS,
                    'effect3': SPELL_EFFECTS,
                    'effectMechanic1': SPELL_EFFECT_MECHANICS,
                    'effectMechanic2': SPELL_EFFECT_MECHANICS,
                    'effectMechanic3': SPELL_EFFECT_MECHANICS,
                    'effectApplyAuraName1': SPELL_AURA_TYPES,
                    'effectApplyAuraName2': SPELL_AURA_TYPES,
                    'effectApplyAuraName3': SPELL_AURA_TYPES,
                    'school': SPELL_SCHOOLS,
                    'dmgClass': SPELL_DAMAGE_CLASS,
                    'powerType': SPELL_POWER_TYPE,
                    'spellFamilyName': SPELL_FAMILY,
                    'dispel': SPELL_DISPEL_TYPE,
                    'mechanic': SPELL_MECHANIC,
                    'targetCreatureType': SPELL_TARGET_CREATURE_TYPE,
                    'preventionType': SPELL_PREVENTION_TYPE,
                    'procFlags': SPELL_PROC_FLAGS,
                    'rangeIndex': SPELL_RANGE,
                    'durationIndex': SPELL_DURATION,
                    'castingTimeIndex': SPELL_CAST_TIME,
                    'targetAuraState': SPELL_AURA_STATE,
                    'casterAuraState': SPELL_AURA_STATE,
                    'effectRadiusIndex1': SPELL_RADIUS,
                    'effectRadiusIndex2': SPELL_RADIUS,
                    'effectRadiusIndex3': SPELL_RADIUS,
                    'effectImplicitTargetA1': SPELL_IMPLICIT_TARGETS,
                    'effectImplicitTargetA2': SPELL_IMPLICIT_TARGETS,
                    'effectImplicitTargetA3': SPELL_IMPLICIT_TARGETS,
                    'effectImplicitTargetB1': SPELL_IMPLICIT_TARGETS,
                    'effectImplicitTargetB2': SPELL_IMPLICIT_TARGETS,
                    'effectImplicitTargetB3': SPELL_IMPLICIT_TARGETS,
                    'customFlags': SPELL_CUSTOM_FLAGS,
                }[field_name]
                
                if field_name in bit_flag_fields:
                    # 位标志字段 - 使用位运算
                    flags = parse_spell_flags(value, flag_dict)
                    html = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: "Microsoft YaHei", Arial; }}
                            .value {{ color: #666; margin: 10px 0; }}
                            .flag {{ margin: 5px 0; }}
                            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                            th {{ background-color: #f5f5f5; }}
                            .section-title {{ font-weight: bold; margin: 15px 0 5px 0; }}
                        </style>
                    </head>
                    <body>
                        <div class="value">当前值: {value} (0x{value:X})</div>
                        <div class="section-title">激活的标志:</div>
                        {''.join(f'<div class="flag">- {flag}</div>' for flag in flags)}
                        
                        <div class="section-title">所有可用标志:</div>
                        <table>
                            <tr>
                                <th>位值</th>
                                <th>名称</th>
                                <th>描述</th>
                            </tr>
                            {''.join(f'''
                            <tr>
                                <td>0x{bit:08X}</td>
                                <td>{desc.split(" - ")[0]}</td>
                                <td>{desc.split(" - ")[1] if " - " in desc else ""}</td>
                            </tr>
                            ''' for bit, desc in flag_dict.items())}
                        </table>
                    </body>
                    </html>
                    """
                else:
                    # 枚举字段 - 直接匹配值
                    description = flag_dict.get(value, f"未知值: {value}")
                    html = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: "Microsoft YaHei", Arial; }}
                            .value {{ color: #666; margin: 10px 0; }}
                            .current {{ margin: 10px 0; }}
                            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                            th {{ background-color: #f5f5f5; }}
                            .section-title {{ font-weight: bold; margin: 15px 0 5px 0; }}
                        </style>
                    </head>
                    <body>
                        <div class="current">当前值: {value}</div>
                        <div class="current">描述: {description}</div>
                        
                        <div class="section-title">所有可用值:</div>
                        <table>
                            <tr>
                                <th>值</th>
                                <th>名���</th>
                                <th>描述</th>
                            </tr>
                            {''.join(f'''
                            <tr>
                                <td>{val}</td>
                                <td>{desc.split(" - ")[0]}</td>
                                <td>{desc.split(" - ")[1] if " - " in desc else ""}</td>
                            </tr>
                            ''' for val, desc in flag_dict.items())}
                        </table>
                    </body>
                    </html>
                    """
                
                self.info_text.setHtml(html)
            else:
                # 显示字段类型
                field_type = SPELL_FIELDS.get(field_name, 'unknown')
                self.info_text.setHtml(f'<div>类型: {field_type}</div>')
                
        except Exception as e:
            self.info_text.setHtml(f'<div>错误: {str(e)}</div>')

    def compareData(self):
        """数据对比功能"""
        if not self.current_entry:
            QMessageBox.warning(self, '警告', '请先加载当前数据')
            return
        
        # 创建对比对话框
        dialog = QDialog(self)
        dialog.setWindowTitle('数据对比')
        layout = QVBoxLayout(dialog)
        
        # 添加历史记录下拉框
        history_combo = QComboBox()
        history_combo.addItem("新建对比...")
        for hist in self.compare_history:
            history_combo.addItem(f"Entry: {hist['entry']}, Build: {hist['build']}")
        
        layout.addWidget(QLabel("选择历史记:"))
        layout.addWidget(history_combo)
        
        # 创建输入���域
        input_widget = QWidget()
        input_layout = QFormLayout(input_widget)
        entry_input = QLineEdit()
        build_input = QLineEdit('5875')
        input_layout.addRow('对比Entry:', entry_input)
        input_layout.addRow('对比Build:', build_input)
        layout.addWidget(input_widget)
        
        # 根据下拉框选择显示/隐藏输入区域
        def on_combo_changed(index):
            input_widget.setVisible(index == 0)
            if index > 0:
                # 填充历史记录数据
                hist = self.compare_history[index - 1]
                entry_input.setText(str(hist['entry']))
                build_input.setText(str(hist['build']))
        
        history_combo.currentIndexChanged.connect(on_combo_changed)
        
        # 添加钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                compare_entry = int(entry_input.text())
                compare_build = int(build_input.text())
                
                # 查对比数据
                self.cursor.execute(
                    "SELECT * FROM spell_template WHERE entry = %s AND build = %s",
                    (compare_entry, compare_build))
                compare_result = self.cursor.fetchone()
                
                if compare_result:
                    # 添加到历史记录
                    new_history = {
                        'entry': compare_entry,
                        'build': compare_build,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # 检查是否已存在
                    exists = False
                    for hist in self.compare_history:
                        if hist['entry'] == compare_entry and hist['build'] == compare_build:
                            exists = True
                            break
                    
                    if not exists:
                        self.compare_history.insert(0, new_history)
                        # 保持历史记录在最大数量以内
                        self.compare_history = self.compare_history[:self.max_history]
                    
                    # 显示对比结果
                    self.showCompareResult(compare_result)
                else:
                    QMessageBox.warning(self, '警告', '未找到对比数据')
                    
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入有效的数值')

    def showCompareResult(self, compare_data):
        """显示对比结果"""
        dialog = QDialog(self)
        dialog.setWindowTitle('对比结果')
        dialog.resize(1000, 600)  # 加大窗口尺寸
        
        layout = QVBoxLayout(dialog)
        
        # 添加对比信息
        info_label = QLabel(f'当前: Entry {self.current_entry} (Build {self.current_build}) vs '
                          f'对比: Entry {compare_data[0]} (Build {compare_data[1]})')
        layout.addWidget(info_label)
        
        # 创建对比表格
        table = QTableWidget()
        table.setColumnCount(4)  # 增加一列显示差异
        table.setHorizontalHeaderLabels(['字名', '当前值', '对比值', '差异'])
        
        # 设置表格样式
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f6f6f6;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        
        # 获取列名
        self.cursor.execute("SHOW COLUMNS FROM spell_template")
        columns = [column[0] for column in self.cursor.fetchall()]
        
        # 获取当前数据
        self.cursor.execute(
            "SELECT * FROM spell_template WHERE entry = %s AND build = %s",
            (self.current_entry, self.current_build))        
        current_data = self.cursor.fetchone()
        
        if current_data:
            # 设置行数
            diff_count = 0
            rows = []
            
            for i, (col, curr, comp) in enumerate(zip(columns, current_data, compare_data)):
                if str(curr) != str(comp):  # 值不同的才显
                    rows.append((col, curr, comp))
                    diff_count += 1
            
            table.setRowCount(diff_count)
            
            # 填充数据
            for row, (field, curr, comp) in enumerate(rows):
                # 字段名
                table.setItem(row, 0, QTableWidgetItem(field))
                
                # 当前值
                curr_item = QTableWidgetItem(str(curr))
                table.setItem(row, 1, curr_item)
                
                # 对比值
                comp_item = QTableWidgetItem(str(comp))
                table.setItem(row, 2, comp_item)
                
                # 如值不同，设置背景色
                if str(curr) != str(comp):
                    curr_item.setBackground(QColor(255, 200, 200))
                    comp_item.setBackground(QColor(200, 255, 200))
                
                # 添加差异说明
                if str(curr) != str(comp):
                    if isinstance(curr, (int, float)) and isinstance(comp, (int, float)):
                        diff = comp - curr
                        diff_text = f"{diff:+d}" if isinstance(diff, int) else f"{diff:+.2f}"
                    else:
                        diff_text = "值不同"
                    diff_item = QTableWidgetItem(diff_text)
                    table.setItem(row, 3, diff_item)
        
        # 添加筛选选项
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("显示:"))
        
        show_all = QRadioButton("所有字段")
        show_diff = QRadioButton("仅差��")
        show_all.setChecked(True)
        
        def update_filter():
            for row in range(table.rowCount()):
                show = (show_all.isChecked() or 
                       table.item(row, 1).text() != table.item(row, 2).text())
                table.setRowHidden(row, not show)
        
        show_all.toggled.connect(update_filter)
        show_diff.toggled.connect(update_filter)
        filter_layout.addWidget(show_all)
        filter_layout.addWidget(show_diff)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        layout.addWidget(table)
        
        # 添加按钮
        button_layout = QHBoxLayout()
        
        # 添加导出按钮
        export_button = QPushButton('导出对比结果')
        export_button.clicked.connect(lambda: self.exportCompareResult(table))
        button_layout.addWidget(export_button)
        
        # 添加关闭按钮
        close_button = QPushButton('关闭')
        close_button.clicked.connect(dialog.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def exportCompareResult(self, table):
        """导出对比结果"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出对比结果",
            f"spell_compare_{self.current_entry}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    # 写��表头
                    headers = []
                    for col in range(table.columnCount()):
                        headers.append(table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # 写入数据
                    for row in range(table.rowCount()):
                        if not table.isRowHidden(row):
                            row_data = []
                            for col in range(table.columnCount()):
                                item = table.item(row, col)
                                row_data.append(item.text() if item else '')
                            writer.writerow(row_data)
                
                QMessageBox.information(self, '成功', f'对比结果已导出到:\n{filename}')
                
            except Exception as e:
                QMessageBox.critical(self, '错误', f'导出失败: {str(e)}')

    def importData(self):
        """导入数据功能"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "选择导入文件",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    # 读取CSV数据
                    import csv
                    reader = csv.reader(f)
                    headers = next(reader)  # 跳过表头
                    
                    data = next(reader)  # 读取数据行
                    
                    # 更新表格数据
                    for col in range(0, self.table.columnCount(), 2):
                        for row in range(self.table.rowCount()):
                            value_item = self.table.item(row, col + 1)
                            if value_item and row < len(data):
                                value_item.setText(data[row * 2 + 1])  # 跳过字段名列
                    
                    QMessageBox.information(self, '成功', '数据已导入')
                    
            except Exception as e:
                QMessageBox.critical(self, '错误', f'导入失败: {str(e)}')

    def copySpell(self):
        """复制法术到新的ID"""
        if not self.current_entry:
            QMessageBox.warning(self, '警告', '请先加载要复制的法术')
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle('复制法术')
        layout = QFormLayout(dialog)
        
        new_entry = QLineEdit()
        new_build = QLineEdit(str(self.current_build))
        
        layout.addRow('新法术ID:', new_entry)
        layout.addRow('Build版本:', new_build)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                new_id = int(new_entry.text())
                new_build_val = int(new_build.text())
                
                # 检查新ID是否已存在
                self.cursor.execute(
                    "SELECT COUNT(*) FROM spell_template WHERE entry = %s AND build = %s",
                    (new_id, new_build_val))
                if self.cursor.fetchone()[0] > 0:
                    QMessageBox.warning(self, '警告', '该法术ID已存在')
                    return
                
                # 先获取所有列名
                self.cursor.execute("SHOW COLUMNS FROM spell_template")
                columns = [column[0] for column in self.cursor.fetchall()]
                
                # 构建INSERT语句
                columns_str = ', '.join(columns)
                placeholders = ', '.join(['%s'] * len(columns))
                
                # 获取源数据
                self.cursor.execute(
                    f"SELECT {columns_str} FROM spell_template WHERE entry = %s AND build = %s",
                    (self.current_entry, self.current_build))
                source_data = list(self.cursor.fetchone())
                
                # 修改entry和build值
                entry_index = columns.index('entry')
                build_index = columns.index('build')
                source_data[entry_index] = new_id
                source_data[build_index] = new_build_val
                
                # 执行插入
                self.cursor.execute(
                    f"INSERT INTO spell_template ({columns_str}) VALUES ({placeholders})",
                    tuple(source_data))
                self.conn.commit()
                
                QMessageBox.information(self, '成功', f'法术已复制到ID: {new_id}')
                
                # 加载新复制的法术
                self.search_entry.setText(str(new_id))
                self.search_build.setText(str(new_build_val))
                self.searchSpell()
                
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入有效的数值')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'复制失败: {str(e)}')
                self.conn.rollback()

    def searchField(self):
        """搜索并定位到指定字段"""
        dialog = QDialog(self)
        dialog.setWindowTitle('查找字段')
        layout = QVBoxLayout(dialog)
        
        # 创建搜索输入框
        search_input = QLineEdit()
        search_input.setPlaceholderText('输入字段名...')
        layout.addWidget(search_input)
        
        # 创建结果列表
        result_list = QListWidget()
        layout.addWidget(result_list)
        
        # 实时搜索
        def on_text_changed(text):
            result_list.clear()
            if text:
                for field_name in SPELL_FIELDS.keys():
                    if text.lower() in field_name.lower():
                        result_list.addItem(field_name)
        
        search_input.textChanged.connect(on_text_changed)
        
        # 双击择字段
        def on_item_double_clicked(item):
            field_name = item.text()
            # 查找字段位置
            field_names = list(SPELL_FIELDS.keys())
            field_idx = field_names.index(field_name)
            rows = self.table.rowCount()
            col = (field_idx // rows) * 2
            row = field_idx % rows
            
            # 选中并滚动到该字段
            self.table.setCurrentCell(row, col)
            self.table.scrollToItem(self.table.item(row, col))
            
            # 显示字段说明
            self.showFieldInfo(field_name)
            
            dialog.accept()
        
        result_list.itemDoubleClicked.connect(on_item_double_clicked)
        
        dialog.exec_()

    def initCategoryView(self):
        """初始化分类视图"""
        # 创建分类树
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabel('字段分类')
        self.category_tree.setMinimumWidth(200)
        
        # 添加分类
        for category, fields in FIELD_CATEGORIES.items():
            category_item = QTreeWidgetItem([category])
            self.category_tree.addTopLevelItem(category_item)
            
            for field in fields:
                field_item = QTreeWidgetItem([field])
                category_item.addChild(field_item)
        
        # 连接点击事件
        self.category_tree.itemClicked.connect(self.onCategoryItemClicked)
        
        return self.category_tree

    def onCategoryItemClicked(self, item, column):
        """处理分类树点击事件"""
        if item.parent():  # 如果是字项
            field_name = item.text(0)
            # 查找并选中对应的
            field_names = list(SPELL_FIELDS.keys())
            if field_name in field_names:
                field_idx = field_names.index(field_name)
                rows = self.table.rowCount()
                col = (field_idx // rows) * 2
                row = field_idx % rows
                
                self.table.setCurrentCell(row, col)
                self.table.scrollToItem(self.table.item(row, col))
                self.showFieldInfo(field_name)

    def validateAndFormatValue(self, field_name, value):
        """验证并格式化字段值"""
        field_type = SPELL_FIELDS.get(field_name)
        
        try:
            if field_type in ['int', 'bigint', 'smallint']:
                # 检查输入格式
                if isinstance(value, str):
                    if '(' in value and '0x' in value:
                        # ���显示格式中提取值 "123 (0x7B)" -> 123
                        value = int(value.split('(')[0].strip())
                    elif '0x' in value.lower():
                        # 处理十六进制字符串
                        value = int(value.replace('0x', ''), 16)
                    else:
                        # 处理十进制字符串
                        value = int(value)
                
                # 范围检查
                if field_type == 'smallint':
                    if value < -32768 or value > 32767:
                        raise ValueError('smallint值范围: -32768 到 32767')
                elif field_type == 'int':
                    if value < -2147483648 or value > 2147483647:
                        raise ValueError('int值范围: -2147483648 到 2147483647')
                
                # 格式显示
                return True, f"{value} (0x{value:X})"
                
            elif field_type == 'float':
                value = float(value)
                return True, str(value)
                
            else:
                return True, str(value)
                
        except ValueError as e:
            return False, str(e)

    def backupData(self):
        """备份当前数据到本地文件"""
        if not self.current_entry or not self.current_build:
            QMessageBox.warning(self, '警告', '没有加载的法术数据')
            return
        
        try:
            # 创建备份目录
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # 生成备份文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'spell_{self.current_entry}_build_{self.current_build}_{timestamp}.json')
            # 获取当前数据
            self.cursor.execute(
                "SELECT * FROM spell_template WHERE entry = %s AND build = %s",
                (self.current_entry, self.current_build))
            self.cursor.fetchone()
            
            if current_data:
                # 获取列名
                self.cursor.execute("SHOW COLUMNS FROM spell_template")
                columns = [column[0] for column in self.cursor.fetchall()]
                
                # 创建数据字典
                data_dict = {
                    'entry': self.current_entry,
                    'build': self.current_build,
                    'backup_time': timestamp,
                    'data': dict(zip(columns, current_data))
                }
                
                # 保存到JSON文件
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data_dict, f, indent=4, ensure_ascii=False)
                
                QMessageBox.information(self, '成功', f'数据已备份到:\n{backup_file}')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'备份失败: {str(e)}')

    def restoreBackup(self):
        """从本地文件恢复备份数据"""
        try:
            # 选择备份文件
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                QMessageBox.warning(self, '告', '没有找到备份目录')
                return
            
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "选择备份文件",
                backup_dir,
                "JSON Files (*.json);;All Files (*)"
            )
            
            if filename:
                # 读取备份数据
                with open(filename, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                
                # 确认恢复
                reply = QMessageBox.question(
                    self, '确认',
                    f'是否恢复Entry: {backup_data["entry"]}, Build: {backup_data["build"]}的备份数据？\n'
                    f'备份时: {backup_data["backup_time"]}',
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # 更新数据库
                    update_fields = []
                    update_values = []
                    
                    for field, value in backup_data['data'].items():
                        if field not in ['entry', 'build']:  # 跳过主键
                            update_fields.append(f"{field} = %s")
                            update_values.append(value)
                    
                    # 添加WHERE条件的值
                    update_values.extend([backup_data['entry'], backup_data['build']])
                    
                    # 执行更新
                    query = f"""
                        UPDATE spell_template 
                        SET {', '.join(update_fields)}
                        WHERE entry = %s AND build = %s
                    """
                    self.cursor.execute(query, update_values)
                    self.conn.commit()
                    
                    QMessageBox.information(self, '成功', '数据恢复')
                    
                    # 重新加载数据
                    self.search_entry.setText(str(backup_data['entry']))
                    self.search_build.setText(str(backup_data['build']))
                    self.searchSpell()
                    
        except Exception as e:
            QMessageBox.critical(self, '错误', f'恢复失败: {str(e)}')
            self.conn.rollback()

    def addFieldHistory(self, field_name, old_value, new_value):
        """添加字值修改历史"""
        if field_name not in self.field_history:
            self.field_history[field_name] = []
        
        history_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'old_value': old_value,
            'new_value': new_value,
            'entry': self.current_entry,
            'build': self.current_build
        }
        
        self.field_history[field_name].insert(0, history_entry)
        
        # 保持历史记录在最大数量以内
        self.field_history[field_name] = self.field_history[field_name][:self.max_field_history]

    def showFieldHistory(self, field_name):
        """显示字段值修改历史"""
        if field_name not in self.field_history or not self.field_history[field_name]:
            QMessageBox.information(self, '提示', '没有修改历史记录')
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f'字段 {field_name} 的修改历史')
        dialog.resize(800, 400)
        layout = QVBoxLayout(dialog)
        
        # 创建历史记录表格
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(['时间', 'Entry', 'Build', '旧值', '新值', '操作'])
        table.setRowCount(len(self.field_history[field_name]))
        
        # 设置表格样式
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f6f6f6;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        
        # 填充数据
        for row, history in enumerate(self.field_history[field_name]):
            # 时间
            table.setItem(row, 0, QTableWidgetItem(history['timestamp']))
            # Entry
            table.setItem(row, 1, QTableWidgetItem(str(history['entry'])))
            # Build
            table.setItem(row, 2, QTableWidgetItem(str(history['build'])))
            # 旧值
            table.setItem(row, 3, QTableWidgetItem(str(history['old_value'])))
            # 新值
            table.setItem(row, 4, QTableWidgetItem(str(history['new_value'])))
            
            # 添加恢复按钮
            restore_button = QPushButton('恢复此值')
            restore_button.clicked.connect(lambda checked, r=row: self.restoreHistoryValue(field_name, self.field_history[field_name][r]['old_value']))
            table.setCellWidget(row, 5, restore_button)
        
        # 设置列宽
        table.setColumnWidth(0, 150)  # 时间列
        table.setColumnWidth(1, 80)   # Entry列
        table.setColumnWidth(2, 80)   # Build列
        table.setColumnWidth(3, 150)  # 旧值列
        table.setColumnWidth(4, 150)  # 新值列
        table.setColumnWidth(5, 100)  # 操作列
        
        layout.addWidget(table)
        
        # 添加关闭按钮
        close_button = QPushButton('关闭')
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.exec_()

    def restoreHistoryValue(self, field_name, value):
        """恢复历史值"""
        try:
            # 查找字段位置
            field_names = list(SPELL_FIELDS.keys())
            field_idx = field_names.index(field_name)
            rows = self.table.rowCount()
            col = (field_idx // rows) * 2
            row = field_idx % rows
            
            # 更新值
            value_item = self.table.item(row, col + 1)
            if value_item:
                value_item.setText(str(value))
                QMessageBox.information(self, '成功', f'已恢复字段 {field_name} 的值')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'恢复失败: {str(e)}')

    def addUndoAction(self, field_name, old_value, new_value, row, col):
        """添加撤销动作"""
        action = {
            'field_name': field_name,
            'old_value': old_value,
            'new_value': new_value,
            'row': row,
            'col': col
        }
        self.undo_stack.append(action)
        # 清空重做栈
        self.redo_stack.clear()
        # 限制撤销栈大小
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)

    def undo(self):
        """撤销操作"""
        if not self.undo_stack:
            return
        
        action = self.undo_stack.pop()
        # 添加到重做栈
        self.redo_stack.append(action)
        
        # 恢复值
        self.table.blockSignals(True)
        value_item = self.table.item(action['row'], action['col'])
        if value_item:
            value_item.setText(str(action['old_value']))
        self.table.blockSignals(False)
        
        self.statusBar().showMessage(f'已撤销 {action["field_name"]} 的修改')

    def redo(self):
        """重操作"""
        if not self.redo_stack:
            return
        
        action = self.redo_stack.pop()
        # 添加到撤销栈
        self.undo_stack.append(action)
        
        # 恢复值
        self.table.blockSignals(True)
        value_item = self.table.item(action['row'], action['col'])
        if value_item:
            value_item.setText(str(action['new_value']))
        self.table.blockSignals(False)
        
        self.statusBar().showMessage(f'已重做 {action["field_name"]} 的修改')

    def setupFieldAutoComplete(self, item, field_name):
        """设置字段值���动补全"""
        if field_name not in self.field_value_history:
            # 从数据库获取该字段的历史值
            try:
                self.cursor.execute(f"""
                    SELECT DISTINCT {field_name} 
                    FROM spell_template 
                    WHERE {field_name} IS NOT NULL 
                    ORDER BY {field_name}
                    LIMIT 100
                """)
                values = [str(row[0]) for row in self.cursor.fetchall()]
                self.field_value_history[field_name] = values
            except:
                self.field_value_history[field_name] = []
        
        completer = QCompleter(self.field_value_history[field_name])
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        
        line_edit = QLineEdit()
        line_edit.setCompleter(completer)
        self.table.setCellWidget(item.row(), item.column(), line_edit)

    def showConfigDialog(self):
        """显示配置管理对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle('配置管理')
        dialog.resize(500, 400)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 数据库配置标签页
        db_tab = QWidget()
        db_layout = QFormLayout(db_tab)
        
        db_config = self.config.get_database_config()
        host_input = QLineEdit(db_config['host'])
        port_input = QSpinBox()
        port_input.setRange(1, 65535)
        port_input.setValue(db_config['port'])
        user_input = QLineEdit(db_config['user'])
        password_input = QLineEdit(db_config['password'])
        password_input.setEchoMode(QLineEdit.Password)
        database_input = QLineEdit(db_config['database'])
        
        db_layout.addRow('主机:', host_input)
        db_layout.addRow('端口:', port_input)
        db_layout.addRow('用户名:', user_input)
        db_layout.addRow('密码:', password_input)
        db_layout.addRow('数据库:', database_input)
        
        # 用户界面标签
        ui_tab = QWidget()
        ui_layout = QFormLayout(ui_tab)
        
        # 主题选择
        theme_combo = QComboBox()
        theme_combo.addItems(['light', 'dark'])
        theme_combo.setCurrentText(self.config.get_preferences()['theme'])
        ui_layout.addRow('主题:', theme_combo)
        
        # 字体小
        font_size = QSpinBox()
        font_size.setRange(8, 24)
        font_size.setValue(self.config.get_preferences()['font_size'])
        ui_layout.addRow('字体大小:', font_size)
        
        # 表格行高
        row_height = QSpinBox()
        row_height.setRange(20, 50)
        row_height.setValue(self.config.get_preferences()['table_row_height'])
        ui_layout.addRow('表格行高:', row_height)
        
        # 重置布局按钮
        reset_layout = QPushButton('重置窗口布局')
        reset_layout.clicked.connect(self.resetLayout)
        ui_layout.addRow(reset_layout)
        
        tab_widget.addTab(ui_tab, '界面设置')
        
        # 用户偏好标签页
        pref_tab = QWidget()
        pref_layout = QFormLayout(pref_tab)
        
        preferences = self.config.get_preferences()
        theme_combo = QComboBox()
        theme_combo.addItems(['light', 'dark'])
        theme_combo.setCurrentText(preferences['theme'])
        
        font_size = QSpinBox()
        font_size.setRange(8, 24)
        font_size.setValue(preferences['font_size'])
        
        row_height = QSpinBox()
        row_height.setRange(20, 50)
        row_height.setValue(preferences['table_row_height'])
        
        pref_layout.addRow('主题:', theme_combo)
        pref_layout.addRow('字体大小:', font_size)
        pref_layout.addRow('表格行高:', row_height)
        
        # 快捷键标签页
        shortcut_tab = QWidget()
        shortcut_layout = QFormLayout(shortcut_tab)
        
        shortcuts = self.config.get_shortcuts()
        shortcut_editors = {}
        for action, key in shortcuts.items():
            editor = QKeySequenceEdit(key)
            shortcut_editors[action] = editor
            shortcut_layout.addRow(f'{action}:', editor)
        
        # 添加标签页
        tab_widget.addTab(db_tab, '数���库连接')
        tab_widget.addTab(pref_tab, '用户偏好')
        tab_widget.addTab(shortcut_tab, '快捷键')
        
        # 添加路径配置标签页
        path_tab = QWidget()
        path_layout = QFormLayout(path_tab)
        
        paths = self.config.get_paths()
        
        # DBC输出目录
        dbc_output_path = QLineEdit(paths.get('dbc_output_path', ''))
        dbc_browse = QPushButton('浏览...')
        dbc_browse.clicked.connect(lambda: self.browsePath(dbc_output_path, '选择服务端VMangos/DATA/5875/DBC目录'))
        dbc_path_layout = QHBoxLayout()
        dbc_path_layout.addWidget(dbc_output_path)
        dbc_path_layout.addWidget(dbc_browse)
        path_layout.addRow('VM/5875/DBC目录:', dbc_path_layout)
        
        # 补丁目录
        patch_path = QLineEdit(paths.get('patch_path', ''))
        patch_browse = QPushButton('浏览...')
        patch_browse.clicked.connect(lambda: self.browsePath(patch_path, '选择要打包的MPQ目录'))
        patch_path_layout = QHBoxLayout()
        patch_path_layout.addWidget(patch_path)
        patch_path_layout.addWidget(patch_browse)
        path_layout.addRow('打包MPQ目录:', patch_path_layout)
        
        # MPQ输出目录
        mpq_output_path = QLineEdit(paths.get('mpq_output_path', ''))
        mpq_browse = QPushButton('浏览...')
        mpq_browse.clicked.connect(lambda: self.browsePath(mpq_output_path, '选择MPQ保存的文件或者路径'))
        mpq_path_layout = QHBoxLayout()
        mpq_path_layout.addWidget(mpq_output_path)
        mpq_path_layout.addWidget(mpq_browse)
        path_layout.addRow('MPQ生成路径:', mpq_path_layout)
        
        tab_widget.addTab(path_tab, '路径设置')
        
        # 创建按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        
        # ���建主布局
        layout = QVBoxLayout(dialog)
        layout.addWidget(tab_widget)
        layout.addWidget(buttons)
        
        # �����接信号
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            # 保存界面设置
            preferences = self.config.get_preferences()
            preferences.update({
                'theme': theme_combo.currentText(),
                'font_size': font_size.value(),
                'table_row_height': row_height.value()
            })
            self.config.set_preferences(preferences)
            
            # 应用新的设置
            self.applyPreferences()
            
            # 保存路径设置
            self.config.set_paths({
                'dbc_output_path': dbc_output_path.text(),
                'patch_path': patch_path.text(), 
                'mpq_output_path': mpq_output_path.text()
            })

    def resetLayout(self):
        """重置窗口布局到默认状态"""
        preferences = self.config.get_preferences()
        preferences.update({
            'window_size': [1920, 1000],
            'column_widths': {},
            'splitter_sizes': []
        })
        self.config.set_preferences(preferences)
        self.restoreLayout()

    def applyPreferences(self):
        """应用用户偏好设置"""
        preferences = self.config.get_preferences()
        
        # 设置字体大小
        font = self.font()
        font.setPointSize(preferences['font_size'])
        self.setFont(font)
        
        # 设置表格行高
        self.table.verticalHeader().setDefaultSectionSize(preferences['table_row_height'])
        
        # 应用主题
        if preferences['theme'] == 'dark':
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QTableWidget {
                    background-color: #363636;
                    color: #ffffff;
                    gridline-color: #505050;
                    alternate-background-color: #404040;
                }
                QTableWidget::item:selected {
                    background-color: #0078d7;
                }
                QTreeWidget {
                    background-color: #363636;
                    color: #ffffff;
                }
                QLabel, QLineEdit, QPushButton {
                    color: #ffffff;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenuBar::item:selected {
                    background-color: #404040;
                }
                QMenu {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenu::item:selected {
                    background-color: #404040;
                }
            """)
        else:
            self.setStyleSheet("")

    def saveLayout(self):
        """保存窗口布局"""
        preferences = self.config.get_preferences()
        
        # 保存窗口大小
        preferences['window_size'] = [self.width(), self.height()]
        
        # 保存列宽
        column_widths = {}
        for col in range(self.table.columnCount()):
            column_widths[str(col)] = self.table.columnWidth(col)
        preferences['column_widths'] = column_widths
        
        # 保存分割器大小
        splitter_sizes = []
        for splitter in self.findChildren(QSplitter):
            splitter_sizes.append([size for size in splitter.sizes()])
        preferences['splitter_sizes'] = splitter_sizes
        
        self.config.set_preferences(preferences)

    def restoreLayout(self):
        """恢复窗口布局"""
        preferences = self.config.get_preferences()
        
        # 恢复窗口大小
        if 'window_size' in preferences:
            self.resize(*preferences['window_size'])
        
        # 恢复列宽
        if 'column_widths' in preferences:
            for col, width in preferences['column_widths'].items():
                self.table.setColumnWidth(int(col), width)
        
        # 恢复分割器大小
        if 'splitter_sizes' in preferences:
            splitters = self.findChildren(QSplitter)
            for splitter, sizes in zip(splitters, preferences['splitter_sizes']):
                splitter.setSizes(sizes)

    def closeEvent(self, event):
        """关闭窗口时保存状态"""
        # 保存窗口状态
        self.saveWindowState()
        # 保存其他布局
        self.saveLayout()
        event.accept()
        
    def saveWindowState(self):
        """保存窗口位置和大小"""
        preferences = self.config.get_preferences()
        preferences.update({
            'window_geometry': {
                'x': self.x(),
                'y': self.y(),
                'width': self.width(),
                'height': self.height(),
            }
        })
        self.config.set_preferences(preferences)
        
    def restoreWindowState(self):
        """恢复窗口位置和��小"""
        preferences = self.config.get_preferences()
        if 'window_geometry' in preferences:
            geometry = preferences['window_geometry']
            self.setGeometry(
                geometry.get('x', 100),
                geometry.get('y', 100),
                geometry.get('width', 1920),
                geometry.get('height', 1000)
            )
        else:
            # 默认窗口大小和位置
            self.setGeometry(100, 100, 1920, 1000)

    # 添加浏览目录方法
    def browsePath(self, line_edit, title):
        path = QFileDialog.getExistingDirectory(self, title)
        if path:
            line_edit.setText(path)

    # 添加���成DBC和MPQ的���法框架
    def generateSpellDBC(self):
        """生成SPELL.DBC文件"""
        try:
            paths = self.config.get_paths()
            dbc_path = paths.get('dbc_output_path')
            patch_path = paths.get('patch_path')
            
            if not dbc_path or not patch_path:
                QMessageBox.warning(self, '警告', '请先在配置中设置DBC输出目录和补丁目录')
                return
                
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dll_path = os.path.join(current_dir, "DBCGenerator.dll")
            
            if not os.path.exists(dll_path):
                QMessageBox.critical(self, '错误', 'DBCGenerator.dll不存在')
                return
                
            # 设置DLL搜索路径
            os.environ['PATH'] = current_dir + os.pathsep + os.environ['PATH']
            os.add_dll_directory(current_dir)
            
            # 加载DLL
            try:
                mydll = ctypes.CDLL(dll_path)
            except Exception as e:
                QMessageBox.critical(self, '错误', f'加载DLL失败: {str(e)}')
                return
                
            # 设置函数参数类型和返回值类型
            mydll.ExportDbcForDll.argtypes = [ctypes.c_char_p]
            mydll.ExportDbcForDll.restype = ctypes.c_int
            
            # 从配置获取数据库连接信息
            db_config = self.config.get_database_config()
            connection_string = f"{db_config['host']};{db_config['port']};{db_config['user']};{db_config['password']};{db_config['database']}"
            
            # 调用DLL函数
            result = mydll.ExportDbcForDll(connection_string.encode('utf-8'))
            
            if result == 1:
                # DBC生成成功,复制到指定目录
                source_dbc = os.path.join(current_dir, "Spell.dbc")
                if os.path.exists(source_dbc):
                    try:
                        # 复制到DBC输出目录
                        os.makedirs(dbc_path, exist_ok=True)
                        target_dbc = os.path.join(dbc_path, "Spell.dbc")
                        shutil.copy2(source_dbc, target_dbc)
                        
                        # 复制到补丁目录的DBFilesClient下
                        dbfiles_path = os.path.join(patch_path, "DBFilesClient")
                        os.makedirs(dbfiles_path, exist_ok=True)
                        patch_dbc = os.path.join(dbfiles_path, "Spell.dbc")
                        shutil.copy2(source_dbc, patch_dbc)
                        
                        # 删除原始文件
                        os.remove(source_dbc)
                        
                        QMessageBox.information(self, '成功', 
                            f'SPELL.DBC已生成并复制到:\n'
                            f'1. {target_dbc}\n'
                            f'2. {patch_dbc}'
                        )
                        self.statusBar().showMessage('SPELL.DBC生成成功')
                        
                    except Exception as e:
                        QMessageBox.warning(self, '警告', f'复制文件时出错: {str(e)}')
                else:
                    QMessageBox.warning(self, '警告', 'DBC生成成功但文件未找到')
            else:
                QMessageBox.critical(self, '错误', 'DBC生成失败')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成SPELL.DBC失败: {str(e)}')
            self.statusBar().showMessage('SPELL.DBC生成失败')

    def generateMPQ(self):
        """生成MPQ文件"""
        try:
            paths = self.config.get_paths()
            patch_path = paths.get('patch_path')
            mpq_path = paths.get('mpq_output_path')
            
            if not patch_path or not mpq_path:
                QMessageBox.warning(self, '警告', '请先在配置中设置补丁目录和MPQ输出目录')
                return
                
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dll_path = os.path.join(current_dir, 'mpqpatcher.dll')
            
            if not os.path.exists(dll_path):
                QMessageBox.critical(self, '错误', 'mpqpatcher.dll不存在')
                return
                
            # 设置DLL搜索路径
            os.environ['PATH'] = current_dir + os.pathsep + os.environ['PATH']
            try:
                os.add_dll_directory(current_dir)
            except:
                pass
            
            # 使用kernel32加载DLL
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            old_mode = kernel32.SetErrorMode(0x8001)  # 禁用错误对话框
            
            try:
                handle = kernel32.LoadLibraryExW(dll_path, None, 0x00000008)
                if handle:
                    mpq_dll = ctypes.WinDLL(dll_path, handle=handle)
                    
                    # 设置函数参数类型
                    mpq_dll.run_str.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
                    mpq_dll.run_str.restype = ctypes.c_int
                    
                    # 准备路径 - 使用完整路径并确保使用双反斜杠
                    mpq_file_path = mpq_path.replace('/', '\\')  # 直接使用配置的MPQ路径
                    source_dir_path = patch_path.replace('/', '\\')
                    
                    # 确保目录存在
                    os.makedirs(os.path.dirname(mpq_file_path), exist_ok=True)
                    
                    # 调用DLL函数
                    result = mpq_dll.run_str(
                        mpq_file_path.encode('utf-8'),
                        source_dir_path.encode('utf-8')
                    )
                    
                    if result == 0:
                        QMessageBox.information(self, '成功', 
                            f'MPQ文件已生成到:\n{mpq_file_path}'
                        )
                        self.statusBar().showMessage('MPQ生成成功')
                    else:
                        QMessageBox.critical(self, '错误', 'MPQ生成失��')
                else:
                    error = ctypes.get_last_error()
                    QMessageBox.critical(self, '错误', f'加载DLL失败: 错误码 {error}')
                    
            finally:
                kernel32.SetErrorMode(old_mode)  # 恢复错误模式
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成MPQ失败: {str(e)}')
            self.statusBar().showMessage('MPQ生成失败')

    def showAdvancedSearch(self):
        """显示高级搜索对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle('高级搜索')
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)
        
        # 创建搜索条件区域
        search_group = QGroupBox("搜索条件")
        search_layout = QGridLayout()
        
        # 定义要搜索的字段
        search_fields = [
            ('effect1', 'Effect 1', SPELL_EFFECTS),
            ('effect2', 'Effect 2', SPELL_EFFECTS),
            ('effect3', 'Effect 3', SPELL_EFFECTS),
            ('effectApplyAuraName1', 'Aura 1', SPELL_AURA_TYPES),
            ('effectApplyAuraName2', 'Aura 2', SPELL_AURA_TYPES),
            ('effectApplyAuraName3', 'Aura 3', SPELL_AURA_TYPES),
        ]
        
        # 创建搜索输入框和提示列表
        self.search_inputs = {}
        self.search_lists = {}
        
        for row, (field, label, values_dict) in enumerate(search_fields):
            # 标签
            search_layout.addWidget(QLabel(label), row, 0)
            
            # 输入框
            input_widget = QLineEdit()
            input_widget.setPlaceholderText('输入ID或描述...')
            search_layout.addWidget(input_widget, row, 1)
            self.search_inputs[field] = input_widget
            
            # 结果列表
            list_widget = QListWidget()
            list_widget.setHidden(True)
            list_widget.setMaximumHeight(150)
            search_layout.addWidget(list_widget, row, 2)
            self.search_lists[field] = list_widget
            
            # 为每个输入框添加文本变化事件
            def create_text_changed(field_name, values):
                def on_text_changed(text):
                    list_widget = self.search_lists[field_name]
                    list_widget.clear()
                    
                    if text:
                        # 搜索匹配项
                        for value, desc in values.items():
                            if (text.isdigit() and str(value) == text) or \
                               text.lower() in desc.lower():
                                item = QListWidgetItem(f"{value}: {desc}")
                                item.setData(Qt.UserRole, value)
                                list_widget.addItem(item)
                        
                        # 显示/隐藏列表
                        list_widget.setHidden(list_widget.count() == 0)
                    else:
                        list_widget.setHidden(True)
                
                return on_text_changed
            
            input_widget.textChanged.connect(create_text_changed(field, values_dict))
            
            # 为列表添加点击事件
            def create_item_clicked(input_widget):
                def on_item_clicked(item):
                    value = item.data(Qt.UserRole)
                    input_widget.setText(str(value))
                    self.search_lists[field].setHidden(True)
                return on_item_clicked
            
            list_widget.itemClicked.connect(create_item_clicked(input_widget))
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # 添加搜索按钮
        button_layout = QHBoxLayout()
        search_button = QPushButton('搜索')
        search_button.clicked.connect(lambda: self.performAdvancedSearch(dialog))
        button_layout.addWidget(search_button)
        
        cancel_button = QPushButton('取消')
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def performAdvancedSearch(self, dialog):
        """执行高级搜索"""
        try:
            # 构建搜索条件
            conditions = []
            values = []
            
            for field, input_widget in self.search_inputs.items():
                text = input_widget.text().strip()
                if text:
                    try:
                        value = int(text)
                        conditions.append(f"{field} = %s")
                        values.append(value)
                    except ValueError:
                        continue
            
            if not conditions:
                QMessageBox.warning(self, '警告', '请至少输入���个搜索条件')
                return
            
            # 构建SQL查询
            query = f"""
                SELECT DISTINCT entry, build, name 
                FROM spell_template 
                WHERE {' OR '.join(conditions)}
                ORDER BY entry, build
            """
            
            # 行查询
            self.cursor.execute(query, values)
            results = self.cursor.fetchall()
            
            if results:
                # 显示结果对话框
                result_dialog = QDialog(self)
                result_dialog.setWindowTitle('搜索结果')
                result_dialog.resize(400, 500)
                layout = QVBoxLayout(result_dialog)
                
                # 创建结果表格
                table = QTableWidget()
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(['Entry', 'Build', 'Name'])
                table.setRowCount(len(results))
                
                for row, (entry, build, name) in enumerate(results):
                    table.setItem(row, 0, QTableWidgetItem(str(entry)))
                    table.setItem(row, 1, QTableWidgetItem(str(build)))
                    table.setItem(row, 2, QTableWidgetItem(str(name)))
                
                # 调整列宽
                table.resizeColumnsToContents()
                
                # 双击加载法术
                def on_double_click(item):
                    row = item.row()
                    entry = int(table.item(row, 0).text())
                    build = int(table.item(row, 1).text())
                    self.search_entry.setText(str(entry))
                    self.search_build.setText(str(build))
                    self.searchSpell()
                    result_dialog.accept()
                    dialog.accept()
                
                table.itemDoubleClicked.connect(on_double_click)
                
                layout.addWidget(table)
                
                # 添加关闭按钮
                close_button = QPushButton('关闭')
                close_button.clicked.connect(result_dialog.accept)
                layout.addWidget(close_button)
                
                result_dialog.exec_()
            else:
                QMessageBox.information(self, '提示', '未找到匹配的法术')
        
        except Exception as e:
            QMessageBox.critical(self, '错误', f'搜索失败: {str(e)}')

    # 在显示对话框时设置图标
    def showDialog(self):
        dialog = QDialog(self)
        dialog.setWindowIcon(self.windowIcon())  # 使用主窗口的图标

def center_window(window):
    """将窗口移动到屏幕中央"""
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    x = (screen.width() - size.width()) // 2
    y = (screen.height() - size.height()) // 2
    # 确保窗口不会太靠上，至少留出标题栏的空间
    y = max(y, 50)  
    window.move(x, y)

def load_license_key():
    """从本地文件加载许可证密钥"""
    license_file = "license.json"
    if os.path.exists(license_file):
        try:
            with open(license_file, 'r') as f:
                data = json.load(f)
                return data.get('key')
        except:
            return None
    return None

def save_license_key(key):
    """保存许可证密钥到本地���件"""
    license_file = "license.json"
    try:
        with open(license_file, 'w') as f:
            json.dump({'key': key}, f)
        return True
    except:
        return False

# 添加一些关键数据的加密函数
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

# 修改许可证相关的代码
class LicenseManager:
    def __init__(self):
        # 使用硬件信息生成唯一密钥
        self._hw_id = self._get_hardware_id()
        self._key = base64.urlsafe_b64encode(hashlib.sha256(self._hw_id.encode()).digest())
        
    def _get_hardware_id(self):
        """获取硬件信息的混合值"""
        try:
            import wmi
            c = wmi.WMI()
            # 混合多个硬件信息
            cpu_id = c.Win32_Processor()[0].ProcessorId
            bios_id = c.Win32_BIOS()[0].SerialNumber
            disk_id = c.Win32_DiskDrive()[0].SerialNumber
            return hashlib.sha256(f"{cpu_id}{bios_id}{disk_id}".encode()).hexdigest()
        except:
            return Helpers.GetMachineCode()

    def save_license(self, key):
        """加密保存许可证"""
        try:
            encrypted_key = encrypt_data(key, self._key)
            checksum = hashlib.sha256(encrypted_key.encode()).hexdigest()
            data = {
                'k': encrypted_key,
                'h': checksum,
                'v': base64.b64encode(self._hw_id.encode()).decode()
            }
            with open("license.dat", 'w') as f:  # 改用不明显的扩展名
                json.dump(data, f)
            return True
        except:
            return False

    def load_license(self):
        """解密加载许可证"""
        try:
            if not os.path.exists("license.dat"):
                return None
                
            with open("license.dat", 'r') as f:
                data = json.load(f)
                
            # 验证硬件信息和校验和
            if data['h'] != hashlib.sha256(data['k'].encode()).hexdigest():
                return None
                
            stored_hw = base64.b64decode(data['v'].encode()).decode()
            if stored_hw != self._hw_id:
                return None
                
            return decrypt_data(data['k'], self._key)
        except:
            return None

# 添加反调试和完整性检查
def check_environment():
    """检查运行环境"""
    try:
        # 基本检查
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return False
            
        # 检测虚拟机
        try:
            import wmi
            c = wmi.WMI()
            for item in c.Win32_ComputerSystem():
                if any(x in item.Model.lower() for x in ['virtual', 'vmware', 'vbox']):
                    return False
        except:
            pass
            
        # 检测常见调试工具进程
        suspicious_processes = [
            'x32dbg.exe', 'x64dbg.exe', 'ollydbg.exe', 'ida.exe', 
            'ida64.exe', 'radare2.exe', 'windbg.exe'
        ]
        
        import wmi
        c = wmi.WMI()
        running_processes = [p.Name.lower() for p in c.Win32_Process()]
        if any(p in running_processes for p in suspicious_processes):
            return False
            
        # 检测系统时间异常
        start_time = time.time()
        time.sleep(0.1)
        end_time = time.time()
        if end_time - start_time > 0.5:  # 时间流逝异常
            return False
            
        return True
    except:
        return True  # 如果检查过程出错，允许程序运行

# 在主程序开始时添加检查
if __name__ == '__main__':
    if not check_environment():
        sys.exit()

# 修改主程序验证部分
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    app_icon = QIcon("app.ico")
    app.setWindowIcon(app_icon)
    
    # 强制使用英文
    app.setProperty('defaultLocale', 'en')
    app.setApplicationName('SpellEditor')
    
    # 确保 Qt 能找到插件
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的路径
        qt_plugin_path = os.path.join(sys._MEIPASS, 'platforms')
    else:
        # 开发环境路径
        qt_plugin_path = os.path.join(os.path.dirname(__file__), 'platforms')
    
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
    
    # 使用许可证管理器
    license_manager = LicenseManager()
    license_key = license_manager.load_license()
    
    if not license_key:
        # 如果没有本地密钥,显示输入对话框
        key_dialog = QDialog()
        key_dialog.setWindowTitle('输入许可证密钥')
        key_dialog.setFixedSize(400, 150)  # 设置固定大小
        layout = QVBoxLayout()
        
        # 添加说明标签
        info_label = QLabel('请输入有效的许可证密钥:')
        info_label.setStyleSheet('padding: 10px;')
        layout.addWidget(info_label)
        
        # 输入框
        key_input = QLineEdit()
        key_input.setPlaceholderText('请输入许可证密钥')
        key_input.setStyleSheet('padding: 5px; margin: 5px;')
        layout.addWidget(key_input)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(key_dialog.accept)
        button_box.rejected.connect(key_dialog.reject)
        button_box.setStyleSheet('padding: 10px;')
        layout.addWidget(button_box)
        
        key_dialog.setLayout(layout)
        
        # 将对话框移到屏幕中央
        center_window(key_dialog)
        
        if key_dialog.exec_() == QDialog.Accepted:
            license_key = key_input.text().strip()
        else:
            sys.exit()

    # 验证许可证
    try:
        result = Key.activate(
            token=auth,
            rsa_pub_key=RSAPubKey,
            product_id=28151,  # 新的product_id
            key=license_key,
            machine_code=Helpers.GetMachineCode()
        )

        if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
            # 显示更详细的错误信息
            error_msg = "许可证验证失败:\n"
            if result[0] == None:
                error_msg += "- 无效的许可证密钥\n"
            else:
                error_msg += "- 许可证不匹配当前机器\n"
            error_msg += "\n请确保输入了正确的许可证密钥。"
            
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle('错误')
            error_dialog.setText(error_msg)
            error_dialog.setStandardButtons(QMessageBox.Ok)
            center_window(error_dialog)
            error_dialog.exec_()
            
            # 删除无效的许可证文件
            if os.path.exists('license.dat'):
                os.remove('license.dat')
            sys.exit()
        else:
            # 保存加密的许可证
            if not license_manager.load_license():
                license_manager.save_license(license_key)
            
            # 显示许可证信息
            license_info = result[0]
            print("许可证有效!过期时间:", license_info.expires)
            
            # 启动主程序
            editor = SpellDatabaseEditor()
            
            # 尝试恢复上次的窗口位置
            config = Config()
            preferences = config.get_preferences()
            if 'window_geometry' in preferences:
                geometry = preferences['window_geometry']
                editor.setGeometry(
                    geometry.get('x', 100),
                    geometry.get('y', 100),
                    geometry.get('width', 1920),
                    geometry.get('height', 1000)
                )
            else:
                # 如果没有保存的位置，则居中显示
                center_window(editor)
                
            editor.show()
            sys.exit(app.exec_())
            
    except Exception as e:
        # 更详细的错误信息
        error_msg = f"验证许可证时发生错误:\n{str(e)}\n\n"
        error_msg += "可能的原因:\n"
        error_msg += "1. 网络连接问题\n"
        error_msg += "2. 许可证服务器暂时不可用\n"
        error_msg += "3. 许可证密钥格式错误\n"
        error_msg += "\n请检查网络连接并重试。"
        
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle('错误')
        error_dialog.setText(error_msg)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        center_window(error_dialog)
        error_dialog.exec_()
        sys.exit()
