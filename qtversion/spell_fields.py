from logger import logger

# 定义所有字段及其类型
SPELL_FIELDS = {
    'entry': 'smallint',  # 法术ID
    'build': 'smallint',  # 客户端版本号
    'school': 'int',  # 法术学派
    'category': 'int',  # 法术分类
    'castUI': 'int',  # 施法界面
    'dispel': 'int',  # 驱散类型
    'mechanic': 'int',  # 机制类型
    'attributes': 'int',  # 属性标志
    'attributesEx': 'int',  # 扩展属性标志1
    'attributesEx2': 'int',  # 扩展属性标志2
    'attributesEx3': 'int',  # 扩展属性标志3
    'attributesEx4': 'int',  # 扩展属性标志4
    'stances': 'int',  # 可用姿态
    'stancesNot': 'int',  # 不可用姿态
    'targets': 'int',  # 目标标志
    'targetCreatureType': 'int',  # 目标生物类型
    'requiresSpellFocus': 'int',  # 需要法术焦点
    'casterAuraState': 'int',  # 施法者光环状态
    'targetAuraState': 'int',  # 目标光环状态
    'castingTimeIndex': 'int',  # 施法时间索引
    'recoveryTime': 'int',  # 恢复时间
    'categoryRecoveryTime': 'int',  # 分类恢复时间
    'interruptFlags': 'int',  # 打断标志
    'auraInterruptFlags': 'int',  # 光环打断标志
    'channelInterruptFlags': 'int',  # 引导打断标志
    'procFlags': 'int',  # 触发标志
    'procChance': 'int',  # 触发几率
    'procCharges': 'int',  # 触发次数
    'maxLevel': 'int',  # 最高等级
    'baseLevel': 'int',  # 基础等级
    'spellLevel': 'int',  # 法术等级
    'durationIndex': 'int',  # 持续时间索引
    'powerType': 'int',  # 能量类型
    'manaCost': 'int',  # 法力消耗
    'manaCostPerLevel': 'int',  # 每级法力消耗
    'manaPerSecond': 'int',  # 每秒法力消耗
    'manaPerSecondPerLevel': 'int',  # 每级每秒法力消耗
    'rangeIndex': 'int',  # 范围索引
    'speed': 'float',  # 法术速度
    'modelNextSpell': 'int',  # 下一个法术模型
    'stackAmount': 'int',  # 堆叠数量
    'totem1': 'int',  # 图腾1
    'totem2': 'int',  # 图腾2
    'reagent1': 'int',  # 材料1
    'reagent2': 'int',  # 材料2
    'reagent3': 'int',  # 材料3
    'reagent4': 'int',  # 材料4
    'reagent5': 'int',  # 材料5
    'reagent6': 'int',  # 材料6
    'reagent7': 'int',  # 材料7
    'reagent8': 'int',  # 材料8
    'reagentCount1': 'int',  # 材料1数量
    'reagentCount2': 'int',  # 材料2数量
    'reagentCount3': 'int',  # 材料3数量
    'reagentCount4': 'int',  # 材料4数量
    'reagentCount5': 'int',  # 材料5数量
    'reagentCount6': 'int',  # 材料6数量
    'reagentCount7': 'int',  # 材料7数量
    'reagentCount8': 'int',  # 材料8数量
    'equippedItemClass': 'int',  # 需要装备类型
    'equippedItemSubClassMask': 'int',  # 需要装备子类型掩码
    'equippedItemInventoryTypeMask': 'int',  # 需要装备栏位掩码
    'effect1': 'int',  # 效果1
    'effect2': 'int',  # 效果2
    'effect3': 'int',  # 效果3
    'effectDieSides1': 'int',  # 效果1骰子面数
    'effectDieSides2': 'int',  # 效果2骰子面数
    'effectDieSides3': 'int',  # 效果3骰子面数
    'effectBaseDice1': 'int',  # 效果1基础骰子数
    'effectBaseDice2': 'int',  # 效果2基础骰子数
    'effectBaseDice3': 'int',  # 效果3基础骰子数
    'effectDicePerLevel1': 'float',  # 效果1每级骰子数
    'effectDicePerLevel2': 'float',  # 效果2每级骰子数
    'effectDicePerLevel3': 'float',  # 效果3每级骰子数
    'effectRealPointsPerLevel1': 'float',  # 效果1每级实际点数
    'effectRealPointsPerLevel2': 'float',  # 效果2每级实际点数
    'effectRealPointsPerLevel3': 'float',  # 效果3每级实际点数
    'effectBasePoints1': 'int',  # 效果1基础点数
    'effectBasePoints2': 'int',  # 效果2基础点数
    'effectBasePoints3': 'int',  # 效果3基础点数
    'effectMechanic1': 'int',  # 效果1机制
    'effectMechanic2': 'int',  # 效果2机制
    'effectMechanic3': 'int',  # 效果3机制
    'effectImplicitTargetA1': 'int',  # 效果1隐含目标A
    'effectImplicitTargetA2': 'int',  # 效果2隐含目标A
    'effectImplicitTargetA3': 'int',  # 效果3隐含目标A
    'effectImplicitTargetB1': 'int',  # 效果1隐含目标B
    'effectImplicitTargetB2': 'int',  # 效果2隐含目标B
    'effectImplicitTargetB3': 'int',  # 效果3隐含目标B
    'effectRadiusIndex1': 'int',  # 效果1半径索引
    'effectRadiusIndex2': 'int',  # 效果2半径索引
    'effectRadiusIndex3': 'int',  # 效果3半径索引
    'effectApplyAuraName1': 'int',  # 效果1光环名称
    'effectApplyAuraName2': 'int',  # 效果2光环名称
    'effectApplyAuraName3': 'int',  # 效果3光环名称
    'effectAmplitude1': 'int',  # 效果1周期
    'effectAmplitude2': 'int',  # 效果2周期
    'effectAmplitude3': 'int',  # 效果3周期
    'effectMultipleValue1': 'float',  # 效果1倍数值
    'effectMultipleValue2': 'float',  # 效果2倍数值
    'effectMultipleValue3': 'float',  # 效果3倍数值
    'effectChainTarget1': 'int',  # 效果1连锁目标数
    'effectChainTarget2': 'int',  # 效果2连锁目标数
    'effectChainTarget3': 'int',  # 效果3连锁目标数
    'effectItemType1': 'bigint',  # 效果1物品类型
    'effectItemType2': 'bigint',  # 效果2物品类型
    'effectItemType3': 'bigint',  # 效果3物品类型
    'effectMiscValue1': 'int',  # 效果1杂项值
    'effectMiscValue2': 'int',  # 效果2杂项值
    'effectMiscValue3': 'int',  # 效果3杂项值
    'effectTriggerSpell1': 'int',  # 效果1触发法术
    'effectTriggerSpell2': 'int',  # 效果2触发法术
    'effectTriggerSpell3': 'int',  # 效果3触发法术
    'effectPointsPerComboPoint1': 'float',  # 效果1每连击点数值
    'effectPointsPerComboPoint2': 'float',  # 效果2每连击点数值
    'effectPointsPerComboPoint3': 'float',  # 效果3每连击点数值
    'spellVisual1': 'int',  # 法术视觉效果1
    'spellVisual2': 'int',  # 法术视觉效果2
    'spellIconId': 'int',  # 法术图标ID
    'activeIconId': 'int',  # 激活图标ID
    'spellPriority': 'int',  # 法术优先级
    'name': 'varchar',  # 法术名称
    'nameFlags': 'int',  # 名称标志
    'nameSubtext': 'varchar',  # 名称子文本
    'nameSubtextFlags': 'int',  # 名称子文本标志
    'description': 'varchar',  # 法术描述
    'descriptionFlags': 'int',  # 描述标志
    'auraDescription': 'varchar',  # 光环描述
    'auraDescriptionFlags': 'int',  # 光环描述标志
    'manaCostPercentage': 'int',  # 法力消耗百分比
    'startRecoveryCategory': 'int',  # 开始恢复分类
    'startRecoveryTime': 'int',  # 开始恢复时间
    'minTargetLevel': 'int',  # 最低目标等级
    'maxTargetLevel': 'int',  # 最高目标等级
    'spellFamilyName': 'int',  # 法术族名称
    'spellFamilyFlags': 'bigint',  # 法术族标志
    'maxAffectedTargets': 'int',  # 最大影响目标数
    'dmgClass': 'int',  # 伤害类型
    'preventionType': 'int',  # 防护类型
    'stanceBarOrder': 'int',  # 姿态条顺序
    'dmgMultiplier1': 'float',  # 伤害倍数1
    'dmgMultiplier2': 'float',  # 伤害倍数2
    'dmgMultiplier3': 'float',  # 伤害倍数3
    'minFactionId': 'int',  # 最低阵营ID
    'minReputation': 'int',  # 最低声望
    'requiredAuraVision': 'int',  # 需要光环视觉
    'customFlags': 'int'  # 自定义标志
}

def parse_spell_flags(value, flag_dict):
    """
    通用的法术标志位解析函数
    
    Args:
        value: 要解析的值(整数)
        flag_dict: 标志位定义字典 {位值: 描述}
        
    Returns:
        list: 激活的标志位描述列表
    """
    try:
        value = int(value)
        flags = []
        
        # 检查每个位是否被设置
        for bit, desc in flag_dict.items():
            if value & bit:
                flags.append(desc)
                
        return flags
    except (ValueError, TypeError):
        return ["错误: 无效的值"]

# 属性标志位定义
SPELL_ATTRIBUTES = {
    0x00000001: "SPELL_ATTR_PROC_FAILURE_BURNS_CHARGE - 施法失败消耗充能",
    0x00000002: "SPELL_ATTR_USES_RANGED_SLOT - 使用远程武器栏",
    0x00000004: "SPELL_ATTR_ON_NEXT_SWING_NO_DAMAGE - 下次挥击无伤害",
    0x00000008: "SPELL_ATTR_NEED_EXOTIC_AMMO - 需要特殊弹药(仅香草版)",
    0x00000010: "SPELL_ATTR_IS_ABILITY - 是能力而非法术",
    0x00000020: "SPELL_ATTR_IS_TRADESKILL - 专业技能",
    0x00000040: "SPELL_ATTR_PASSIVE - 被动技能",
    0x00000080: "SPELL_ATTR_DO_NOT_DISPLAY - 不在法术书显示",
    0x00000100: "SPELL_ATTR_DO_NOT_LOG - 不在战斗记录显示",
    0x00000200: "SPELL_ATTR_HELD_ITEM_ONLY - 需要主手物品",
    0x00000400: "SPELL_ATTR_ON_NEXT_SWING - 下次挥击触发",
    0x00000800: "SPELL_ATTR_WEARER_CASTS_PROC_TRIGGER - 装备者触发",
    0x00001000: "SPELL_ATTR_DAYTIME_ONLY - 仅白天可用",
    0x00002000: "SPELL_ATTR_NIGHT_ONLY - 仅夜晚可用",
    0x00004000: "SPELL_ATTR_ONLY_INDOORS - 仅室内可用",
    0x00008000: "SPELL_ATTR_ONLY_OUTDOORS - 仅室外可用",
    0x00010000: "SPELL_ATTR_NOT_SHAPESHIFT - 不能在变形状态下使用",
    0x00020000: "SPELL_ATTR_ONLY_STEALTHED - 需要潜行状态",
    0x00040000: "SPELL_ATTR_DO_NOT_SHEATH - 不收起武器",
    0x00080000: "SPELL_ATTR_SCALES_WITH_CREATURE_LEVEL - 随生物等级缩放",
    0x00100000: "SPELL_ATTR_CANCELS_AUTO_ATTACK_COMBAT - 取消自动攻击",
    0x00200000: "SPELL_ATTR_NO_ACTIVE_DEFENSE - 无法被闪避/招架/格挡",
    0x00400000: "SPELL_ATTR_TRACK_TARGET_IN_CAST_PLAYER_ONLY - 仅追踪玩家目标",
    0x00800000: "SPELL_ATTR_ALLOW_CAST_WHILE_DEAD - 死亡时可施放",
    0x01000000: "SPELL_ATTR_ALLOW_WHILE_MOUNTED - 骑乘时可施放",
    0x02000000: "SPELL_ATTR_COOLDOWN_ON_EVENT - 事件触发冷却",
    0x04000000: "SPELL_ATTR_AURA_IS_DEBUFF - 负面效果",
    0x08000000: "SPELL_ATTR_ALLOW_WHILE_SITTING - 坐下时可施放",
    0x10000000: "SPELL_ATTR_NOT_IN_COMBAT_ONLY_PEACEFUL - 非战斗状态可用",
    0x20000000: "SPELL_ATTR_NO_IMMUNITIES - 无视免疫",
    0x40000000: "SPELL_ATTR_HEARTBEAT_RESIST - 心跳抵抗",
    0x80000000: "SPELL_ATTR_NO_AURA_CANCEL - 正面效果不可取消"
}

# 扩展属性标志位定义
SPELL_ATTRIBUTES_EX = {
    0x00000001: "SPELL_ATTR_EX_DISMISS_PET_FIRST - 召唤宠物前需要先解散当前宠物",
    0x00000002: "SPELL_ATTR_EX_USE_ALL_MANA - 使用所有法力值",
    0x00000004: "SPELL_ATTR_EX_IS_CHANNELED - 引导法术",
    0x00000008: "SPELL_ATTR_EX_NO_REDIRECTION - 无法被重向",
    0x00000010: "SPELL_ATTR_EX_NO_SKILL_INCREASE - 不增加技能点",
    0x00000020: "SPELL_ATTR_EX_ALLOW_WHILE_STEALTHED - 潜行状态可用",
    0x00000040: "SPELL_ATTR_EX_IS_SELF_CHANNELED - 自身引导",
    0x00000080: "SPELL_ATTR_EX_NO_REFLECTION - 无法被反射",
    0x00000100: "SPELL_ATTR_EX_ONLY_PEACEFUL_TARGETS - 只能对非战斗目标使用",
    0x00000200: "SPELL_ATTR_EX_INITIATES_COMBAT - 开始战斗",
    0x00000400: "SPELL_ATTR_EX_NO_THREAT - 不产生威胁值",
    0x00000800: "SPELL_ATTR_EX_AURA_UNIQUE - 光环唯一",
    0x00001000: "SPELL_ATTR_EX_FAILURE_BREAKS_STEALTH - 施法失败破除潜行",
    0x00002000: "SPELL_ATTR_EX_TOGGLE_FARSIGHT - 切换远视",
    0x00004000: "SPELL_ATTR_EX_TRACK_TARGET_IN_CHANNEL - 引导时跟踪目标",
    0x00008000: "SPELL_ATTR_EX_IMMUNITY_PURGES_EFFECT - 免疫时净化效果",
    0x00010000: "SPELL_ATTR_EX_IMMUNITY_TO_HOSTILE_AND_FRIENDLY_EFFECTS - 对敌我效果都免疫",
    0x00020000: "SPELL_ATTR_EX_NO_AUTOCAST_AI - AI不自动施放",
    0x00040000: "SPELL_ATTR_EX_PREVENTS_ANIM - 阻止动画",
    0x00080000: "SPELL_ATTR_EX_EXCLUDE_CASTER - 排除施法者",
    0x00100000: "SPELL_ATTR_EX_FINISHING_MOVE_DAMAGE - 终结技伤害",
    0x00200000: "SPELL_ATTR_EX_THREAT_ONLY_ON_MISS - 只在未命中时产生威胁",
    0x00400000: "SPELL_ATTR_EX_FINISHING_MOVE_DURATION - 终结技持续时间",
    0x00800000: "SPELL_ATTR_EX_IGNORE_CASTER_AND_TARGET_RESTRICTIONS - 忽略施法者和目标限制",
    0x01000000: "SPELL_ATTR_EX_SPECIAL_SKILLUP - 特殊技能提升",
    0x02000000: "SPELL_ATTR_EX_UNK25 - 未知25",
    0x04000000: "SPELL_ATTR_EX_REQUIRE_ALL_TARGETS - 需要所有目标",
    0x08000000: "SPELL_ATTR_EX_DISCOUNT_POWER_ON_MISS - 未命中时返还能量",
    0x10000000: "SPELL_ATTR_EX_NO_AURA_ICON - 无光环图标",
    0x20000000: "SPELL_ATTR_EX_NAME_IN_CHANNEL_BAR - 引导条显示名称",
    0x40000000: "SPELL_ATTR_EX_COMBO_ON_BLOCK - 格挡时连击点",
    0x80000000: "SPELL_ATTR_EX_CAST_WHEN_LEARNED - 学习时施放"
}

# 扩展属性标志位2定义
SPELL_ATTRIBUTES_EX2 = {
    0x00000001: "SPELL_ATTR_EX2_ALLOW_DEAD_TARGET - 可以以死亡目标为目标",
    0x00000002: "SPELL_ATTR_EX2_NO_SHAPESHIFT_UI - 不在姿态栏显示",
    0x00000004: "SPELL_ATTR_EX2_IGNORE_LINE_OF_SIGHT - 忽略视线",
    0x00000008: "SPELL_ATTR_EX2_ALLOW_LOW_LEVEL_BUFF - 允许低等级增益",
    0x00000010: "SPELL_ATTR_EX2_USE_SHAPESHIFT_BAR - 使用姿态栏",
    0x00000020: "SPELL_ATTR_EX2_AUTO_REPEAT - 自动重复",
    0x00000040: "SPELL_ATTR_EX2_CANNOT_CAST_ON_TAPPED - 不能对已被攻击的目标施放",
    0x00000080: "SPELL_ATTR_EX2_DO_NOT_REPORT_SPELL_FAILURE - 不报告法术失败",
    0x00000100: "SPELL_ATTR_EX2_UNK8 - 未使用",
    0x00000200: "SPELL_ATTR_EX2_UNK9 - 未使用",
    0x00000400: "SPELL_ATTR_EX2_SPECIAL_TAMING_FLAG - 特殊驯服标志",
    0x00000800: "SPELL_ATTR_EX2_NO_TARGET_PER_SECOND_COSTS - 无目标每秒消耗",
    0x00001000: "SPELL_ATTR_EX2_CHAIN_FROM_CASTER - 从施法者开始连锁",
    0x00002000: "SPELL_ATTR_EX2_ENCHANT_OWN_ITEM_ONLY - 只能附魔自己的物品",
    0x00004000: "SPELL_ATTR_EX2_ALLOW_WHILE_INVISIBLE - 隐形时可用",
    0x00008000: "SPELL_ATTR_EX2_ENABLE_AFTER_PARRY - 招架后启用",
    0x00010000: "SPELL_ATTR_EX2_NO_ACTIVE_PETS - 无激活的宠物",
    0x00020000: "SPELL_ATTR_EX2_DO_NOT_RESET_COMBAT_TIMERS - 不重置战斗计时器",
    0x00040000: "SPELL_ATTR_EX2_REQ_DEAD_PET - 需要死亡宠物",
    0x00080000: "SPELL_ATTR_EX2_ALLOW_WHILE_NOT_SHAPESHIFTED - 非变形时可用",
    0x00100000: "SPELL_ATTR_EX2_INITIATE_COMBAT_POST_CAST - 施法后开始战斗",
    0x00200000: "SPELL_ATTR_EX2_FAIL_ON_ALL_TARGETS_IMMUNE - 所有目标免疫时失败",
    0x00400000: "SPELL_ATTR_EX2_NO_INITIAL_THREAT - 无初始威胁",
    0x00800000: "SPELL_ATTR_EX2_PROC_COOLDOWN_ON_FAILURE - 失败时触发冷却",
    0x01000000: "SPELL_ATTR_EX2_ITEM_CAST_WITH_OWNER_SKILL - 使用所有者技能施放物品",
    0x02000000: "SPELL_ATTR_EX2_DONT_BLOCK_MANA_REGEN - 不阻止法力恢复",
    0x04000000: "SPELL_ATTR_EX2_NO_SCHOOL_IMMUNITIES - 无学派免疫",
    0x08000000: "SPELL_ATTR_EX2_IGNORE_WEAPONSKILL - 忽略武器技能",
    0x10000000: "SPELL_ATTR_EX2_NOT_AN_ACTION - 没有动作",
    0x20000000: "SPELL_ATTR_EX2_CANT_CRIT - 不能暴击",
    0x40000000: "SPELL_ATTR_EX2_ACTIVE_THREAT - 主动威胁",
    0x80000000: "SPELL_ATTR_EX2_RETAIN_ITEM_CAST - 保留物品施放"
}

# 扩展属性标志位3定义
SPELL_ATTRIBUTES_EX3 = {
    0x00000001: "SPELL_ATTR_EX3_PVP_ENABLING - PVP启用",
    0x00000002: "SPELL_ATTR_EX3_NO_PROC_EQUIP_REQUIREMENT - 无装备需求触发",
    0x00000004: "SPELL_ATTR_EX3_NO_CASTING_BAR_TEXT - 无施法条文字",
    0x00000008: "SPELL_ATTR_EX3_COMPLETELY_BLOCKED - 完全格挡",
    0x00000010: "SPELL_ATTR_EX3_NO_RES_TIMER - 无复活计时器",
    0x00000020: "SPELL_ATTR_EX3_NO_DURABILITY_LOSS - 无耐久度损失",
    0x00000040: "SPELL_ATTR_EX3_NO_AVOIDANCE - 无法闪避",
    0x00000080: "SPELL_ATTR_EX3_DOT_STACKING_RULE - DOT叠加规则",
    0x00000100: "SPELL_ATTR_EX3_ONLY_ON_PLAYER - 仅对玩家",
    0x00000200: "SPELL_ATTR_EX3_NOT_A_PROC - 不是触发",
    0x00000400: "SPELL_ATTR_EX3_REQUIRES_MAIN_HAND_WEAPON - 需要主手武器",
    0x00000800: "SPELL_ATTR_EX3_ONLY_BATTLEGROUNDS - 仅战场可用",
    0x00001000: "SPELL_ATTR_EX3_ONLY_ON_GHOSTS - 仅对鬼魂",
    0x00002000: "SPELL_ATTR_EX3_HIDE_CHANNEL_BAR - 隐藏引导条",
    0x00004000: "SPELL_ATTR_EX3_HIDE_IN_RAID_FILTER - 在团队过滤中隐藏",
    0x00008000: "SPELL_ATTR_EX3_NORMAL_RANGED_ATTACK - 普通远程攻击",
    0x00010000: "SPELL_ATTR_EX3_SUPPRESS_CASTER_PROCS - 抑制施法者触发",
    0x00020000: "SPELL_ATTR_EX3_SUPPRESS_TARGET_PROCS - 抑制目标触发",
    0x00040000: "SPELL_ATTR_EX3_ALWAYS_HIT - 总是命中",
    0x00080000: "SPELL_ATTR_EX3_INSTANT_TARGET_PROCS - 即时目标触发",
    0x00100000: "SPELL_ATTR_EX3_ALLOW_AURA_WHILE_DEAD - 死亡时允许光环",
    0x00200000: "SPELL_ATTR_EX3_ONLY_PROC_OUTDOORS - 仅在户外触发",
    0x00400000: "SPELL_ATTR_EX3_CASTING_CANCELS_AUTOREPEAT - 施法取消自动重复",
    0x00800000: "SPELL_ATTR_EX3_NO_DAMAGE_HISTORY - 无伤害历史",
    0x01000000: "SPELL_ATTR_EX3_REQUIRES_OFFHAND_WEAPON - 需要副手武器",
    0x02000000: "SPELL_ATTR_EX3_TREAT_AS_PERIODIC - 视为周期性",
    0x04000000: "SPELL_ATTR_EX3_CAN_PROC_FROM_PROCS - 可以从触发中触发",
    0x08000000: "SPELL_ATTR_EX3_ONLY_PROC_ON_CASTER - 仅在施法者身上触发",
    0x10000000: "SPELL_ATTR_EX3_IGNORE_CASTER_AND_TARGET_RESTRICTIONS - 忽略施法者和目标限制",
    0x20000000: "SPELL_ATTR_EX3_IGNORE_CASTER_MODIFIERS - 忽略施法者修正",
    0x40000000: "SPELL_ATTR_EX3_DO_NOT_DISPLAY_RANGE - 不显示范围",
    0x80000000: "SPELL_ATTR_EX3_NOT_ON_AOE_IMMUNE - 不对AOE免疫"
}

# 扩展属性标志位4定义
SPELL_ATTRIBUTES_EX4 = {
    0x00000001: "SPELL_ATTR_EX4_IGNORE_RESISTANCES - 忽略抗性",
    0x00000002: "SPELL_ATTR_EX4_CLASS_TRIGGER_ONLY_ON_TARGET - 职业触发仅对目标",
    0x00000004: "SPELL_ATTR_EX4_AURA_EXPIRES_OFFLINE - 离线时光环过期",
    0x00000008: "SPELL_ATTR_EX4_NO_HELPFUL_THREAT - 无有益威胁",
    0x00000010: "SPELL_ATTR_EX4_NO_HARMFUL_THREAT - 无有害威胁",
    0x00000020: "SPELL_ATTR_EX4_ALLOW_CLIENT_TARGETING - 允许客户端目标选择",
    0x00000040: "SPELL_ATTR_EX4_CANNOT_BE_STOLEN - 无法被偷取",
    0x00000080: "SPELL_ATTR_EX4_CAN_CAST_WHILE_CASTING - 施法时可施法",
    0x00000100: "SPELL_ATTR_EX4_IGNORE_DAMAGE_TAKEN_MODIFIERS - 忽略受到伤害修正",
    0x00000200: "SPELL_ATTR_EX4_COMBAT_FEEDBACK_WHEN_USABLE - 可用时战斗反馈"
}

# 姿态标志位定义
SPELL_STANCES = {
    0x00000001: "FORM_NONE - 通",
    0x00000002: "FORM_CAT - 猎豹形态",
    0x00000004: "FORM_TREE - 形态",
    0x00000008: "FORM_TRAVEL - 旅行形态",
    0x00000010: "FORM_AQUA - 水栖形态",
    0x00000020: "FORM_BEAR - 熊形态",
    0x00000040: "FORM_AMBIENT - 环境形态",
    0x00000080: "FORM_GHOUL - 食鬼形态",
    0x00000100: "FORM_DIREBEAR - 巨熊形态",
    0x00000200: "FORM_CREATUREBEAR - 生物熊形态",
    0x00000400: "FORM_CREATURECAT - 生物猫形态",
    0x00000800: "FORM_GHOSTWOLF - 幽魂狼形态",
    0x00001000: "FORM_BATTLESTANCE - 战斗姿态",
    0x00002000: "FORM_DEFENSIVESTANCE - 防御姿态",
    0x00004000: "FORM_BERSERKERSTANCE - 狂暴姿态",
    0x00008000: "FORM_SHADOW - 暗影形态",
    0x00010000: "FORM_STEALTH - 潜行形态"
}

# 目标标志位定义
SPELL_TARGETS = {
    0x00000001: "TARGET_FLAG_SELF - 自身",
    0x00000002: "TARGET_FLAG_UNUSED1 - 未使用1",
    0x00000004: "TARGET_FLAG_UNIT - 单位",
    0x00000008: "TARGET_FLAG_UNUSED2 - 未使用2",
    0x00000010: "TARGET_FLAG_UNUSED3 - 未使用3",
    0x00000020: "TARGET_FLAG_ITEM - 物品",
    0x00000040: "TARGET_FLAG_SOURCE_LOCATION - 源位置",
    0x00000080: "TARGET_FLAG_DEST_LOCATION - 目标位置",
    0x00000100: "TARGET_FLAG_OBJECT_UNK - 未知对象",
    0x00000200: "TARGET_FLAG_UNIT_UNK - 未知单位",
    0x00000400: "TARGET_FLAG_PVP_CORPSE - PVP尸体",
    0x00000800: "TARGET_FLAG_UNIT_CORPSE - 单位尸体",
    0x00001000: "TARGET_FLAG_OBJECT - 游戏对象",
    0x00002000: "TARGET_FLAG_TRADE_ITEM - 交易品",
    0x00004000: "TARGET_FLAG_STRING - 字符串",
    0x00008000: "TARGET_FLAG_LOCKED - 已锁定",
    0x00010000: "TARGET_FLAG_CORPSE - 尸体"
}

# 中断标志位定义
SPELL_INTERRUPT_FLAGS = {
    0x00000001: "INTERRUPT_FLAG_MOVEMENT - 移动打断",
    0x00000002: "INTERRUPT_FLAG_DAMAGE - 伤害打断",
    0x00000004: "INTERRUPT_FLAG_INTERRUPT - 打断技能打断",
    0x00000008: "INTERRUPT_FLAG_AUTOATTACK - 自动攻击打断",
    0x00000010: "INTERRUPT_FLAG_ABORT_ON_DMG - 受到伤害时中止",
    0x00000020: "INTERRUPT_FLAG_UNK5 - 未知5",
    0x00000040: "INTERRUPT_FLAG_UNK6 - 未知6",
    0x00000080: "INTERRUPT_FLAG_UNK7 - 未知7"
}

# 光环中断标志位定义
SPELL_AURA_INTERRUPT_FLAGS = {
    0x00000001: "AURA_INTERRUPT_FLAG_HOSTILE_ACTION - 受到敌对行为",
    0x00000002: "AURA_INTERRUPT_FLAG_DAMAGE - 受到伤害",
    0x00000004: "AURA_INTERRUPT_FLAG_ACTION - 行动时",
    0x00000008: "AURA_INTERRUPT_FLAG_MOVING - 移动时",
    0x00000010: "AURA_INTERRUPT_FLAG_TURNING - 转向时",
    0x00000020: "AURA_INTERRUPT_FLAG_JUMPING - 跳跃时",
    0x00000040: "AURA_INTERRUPT_FLAG_UNK6 - 未知6",
    0x00000080: "AURA_INTERRUPT_FLAG_UNK7 - 未知7",
    0x00000100: "AURA_INTERRUPT_FLAG_ENTER_COMBAT - 进入战斗",
    0x00000200: "AURA_INTERRUPT_FLAG_LEAVE_COMBAT - 离开战斗",
    0x00000400: "AURA_INTERRUPT_FLAG_UNK10 - 未知10",
    0x00000800: "AURA_INTERRUPT_FLAG_MOUNT - 上坐骑",
    0x00001000: "AURA_INTERRUPT_FLAG_NOT_SEATED - 站立",
    0x00002000: "AURA_INTERRUPT_FLAG_UNK13 - 未知13",
    0x00004000: "AURA_INTERRUPT_FLAG_UNK14 - 未知14",
    0x00008000: "AURA_INTERRUPT_FLAG_UNK15 - 未知15"
}

# 引导中断标志位定义
SPELL_CHANNEL_INTERRUPT_FLAGS = {
    0x00000001: "CHANNEL_FLAG_MOVEMENT - 移动打断",
    0x00000002: "CHANNEL_FLAG_DAMAGE - 伤害打断",
    0x00000004: "CHANNEL_FLAG_INTERRUPT - 打断技能打断",
    0x00000008: "CHANNEL_FLAG_AUTOATTACK - 自动攻击打断",
    0x00000010: "CHANNEL_FLAG_UNK4 - 未知4",
    0x00000020: "CHANNEL_FLAG_UNK5 - 未知5",
    0x00000040: "CHANNEL_FLAG_UNK6 - 未知6",
    0x00000080: "CHANNEL_FLAG_UNK7 - 未知7"
}

# 法术效果类型定义
SPELL_EFFECTS = {
    0: "SPELL_EFFECT_NONE - 无效果",
    1: "SPELL_EFFECT_INSTAKILL - 瞬间击杀",
    2: "SPELL_EFFECT_SCHOOL_DAMAGE - 学派伤害",
    3: "SPELL_EFFECT_DUMMY - 虚拟效果",
    4: "SPELL_EFFECT_PORTAL_TELEPORT - 传送门传送",
    5: "SPELL_EFFECT_TELEPORT_UNITS - 传送单位",
    6: "SPELL_EFFECT_APPLY_AURA - 应用光环",
    7: "SPELL_EFFECT_ENVIRONMENTAL_DAMAGE - 环境伤害",
    8: "SPELL_EFFECT_POWER_DRAIN - 能量吸取",
    9: "SPELL_EFFECT_HEALTH_LEECH - 生命吸取",
    10: "SPELL_EFFECT_HEAL - 治疗",
    11: "SPELL_EFFECT_BIND - 绑定",
    12: "SPELL_EFFECT_PORTAL - 传送门",
    13: "SPELL_EFFECT_RITUAL_BASE - 仪式基础",
    14: "SPELL_EFFECT_RITUAL_SPECIALIZE - 仪式专精",
    15: "SPELL_EFFECT_RITUAL_ACTIVATE_PORTAL - 活传送门",
    16: "SPELL_EFFECT_QUEST_COMPLETE - 完成任务",
    17: "SPELL_EFFECT_WEAPON_DAMAGE_NOSCHOOL - 无学派武器伤害",
    18: "SPELL_EFFECT_RESURRECT - 复活",
    19: "SPELL_EFFECT_ADD_EXTRA_ATTACKS - 增加额外攻击",
    20: "SPELL_EFFECT_DODGE - 闪避",
    21: "SPELL_EFFECT_EVADE - 躲避",
    22: "SPELL_EFFECT_PARRY - 招架",
    23: "SPELL_EFFECT_BLOCK - 格挡",
    24: "SPELL_EFFECT_CREATE_ITEM - 创造物品",
    25: "SPELL_EFFECT_WEAPON - 武器",
    26: "SPELL_EFFECT_DEFENSE - 防御",
    27: "SPELL_EFFECT_PERSISTENT_AREA_AURA - 持续区域光环",
    28: "SPELL_EFFECT_SUMMON - 召唤",
    29: "SPELL_EFFECT_LEAP - 跳跃",
    30: "SPELL_EFFECT_ENERGIZE - 能量充能",
    31: "SPELL_EFFECT_WEAPON_PERCENT_DAMAGE - 武器百分比伤害",
    32: "SPELL_EFFECT_TRIGGER_MISSILE - 触发飞弹",
    33: "SPELL_EFFECT_OPEN_LOCK - 开锁",
    34: "SPELL_EFFECT_TRANSFORM_ITEM - 转化物品",
    35: "SPELL_EFFECT_APPLY_AREA_AURA_PARTY - 应用队伍区域光环",
    36: "SPELL_EFFECT_LEARN_SPELL - 学习法术",
    37: "SPELL_EFFECT_SPELL_DEFENSE - 法术防御",
    38: "SPELL_EFFECT_DISPEL - 驱散",
    39: "SPELL_EFFECT_LANGUAGE - 语言",
    40: "SPELL_EFFECT_DUAL_WIELD - 双持",
    41: "SPELL_EFFECT_JUMP - 跳跃",
    42: "SPELL_EFFECT_JUMP_DEST - 跳跃到目标",
    43: "SPELL_EFFECT_TELEPORT_UNITS_FACE_CASTER - 传送单位面向施法者",
    44: "SPELL_EFFECT_SKILL_STEP - 技能等级",
    45: "SPELL_EFFECT_ADD_HONOR - 增加荣誉",
    46: "SPELL_EFFECT_SPAWN - 生成",
    47: "SPELL_EFFECT_TRADE_SKILL - 商业技能",
    48: "SPELL_EFFECT_STEALTH - 潜行",
    49: "SPELL_EFFECT_DETECT - 侦测",
    50: "SPELL_EFFECT_TRANS_DOOR - 传送门",
    51: "SPELL_EFFECT_FORCE_CRITICAL_HIT - 强制暴击",
    52: "SPELL_EFFECT_GUARANTEE_HIT - 保证命中",
    53: "SPELL_EFFECT_ENCHANT_ITEM - 附魔物品",
    54: "SPELL_EFFECT_ENCHANT_ITEM_TEMPORARY - 临时附魔物品",
    55: "SPELL_EFFECT_TAMECREATURE - 驯服生物",
    56: "SPELL_EFFECT_SUMMON_PET - 召唤宠物",
    57: "SPELL_EFFECT_LEARN_PET_SPELL - 学习宠物技能",
    58: "SPELL_EFFECT_WEAPON_DAMAGE - 武器伤害",
    59: "SPELL_EFFECT_CREATE_RANDOM_ITEM - 创造随机物品",
    60: "SPELL_EFFECT_PROFICIENCY - 熟练度",
    61: "SPELL_EFFECT_SEND_EVENT - 发送事件",
    62: "SPELL_EFFECT_POWER_BURN - 能量燃烧",
    63: "SPELL_EFFECT_THREAT - 威胁",
    64: "SPELL_EFFECT_TRIGGER_SPELL - 触发法术",
    65: "SPELL_EFFECT_APPLY_AREA_AURA_RAID - 应用团队区域光环",
    66: "SPELL_EFFECT_CREATE_MANA_GEM - 创造法力宝石",
    67: "SPELL_EFFECT_HEAL_MAX_HEALTH - 治疗最大生命值",
    68: "SPELL_EFFECT_INTERRUPT_CAST - 打断施法",
    69: "SPELL_EFFECT_DISTRACT - 扰乱",
    70: "SPELL_EFFECT_PULL - 拉近",
    71: "SPELL_EFFECT_PICKPOCKET - 偷窃",
    72: "SPELL_EFFECT_ADD_FARSIGHT - 添加远视",
    73: "SPELL_EFFECT_UNTRAIN_TALENTS - 重置天赋",
    74: "SPELL_EFFECT_APPLY_GLYPH - 应用雕文",
    75: "SPELL_EFFECT_HEAL_MECHANICAL - 治疗机械",
    76: "SPELL_EFFECT_SUMMON_OBJECT_WILD - 召唤野生物体",
    77: "SPELL_EFFECT_SCRIPT_EFFECT - 脚效果",
    78: "SPELL_EFFECT_ATTACK - 攻击",
    79: "SPELL_EFFECT_SANCTUARY - 庇护所",
    80: "SPELL_EFFECT_ADD_COMBO_POINTS - 增加连击点",
    81: "SPELL_EFFECT_CREATE_HOUSE - 创建房屋",
    82: "SPELL_EFFECT_BIND_SIGHT - 绑定视野",
    83: "SPELL_EFFECT_DUEL - 决斗",
    84: "SPELL_EFFECT_STUCK - 卡住",
    85: "SPELL_EFFECT_SUMMON_PLAYER - 召唤玩家",
    86: "SPELL_EFFECT_ACTIVATE_OBJECT - 激活物体",
    87: "SPELL_EFFECT_GAMEOBJECT_DAMAGE - 游戏对象伤害",
    88: "SPELL_EFFECT_GAMEOBJECT_REPAIR - 修理游戏对象",
    89: "SPELL_EFFECT_GAMEOBJECT_SET_DESTRUCTION_STATE - 设置游戏对象破坏状态",
    90: "SPELL_EFFECT_KILL_CREDIT - 击杀计数",
    91: "SPELL_EFFECT_THREAT_ALL - 威胁所有目标",
    92: "SPELL_EFFECT_ENCHANT_HELD_ITEM - 附魔持有物品",
    93: "SPELL_EFFECT_FORCE_DESELECT - 强制取消选择",
    94: "SPELL_EFFECT_SELF_RESURRECT - 自我复活",
    95: "SPELL_EFFECT_SKINNING - 剥皮",
    96: "SPELL_EFFECT_CHARGE - 冲锋",
    97: "SPELL_EFFECT_CAST_BUTTON - 施法按钮",
    98: "SPELL_EFFECT_KNOCK_BACK - 击退",
    99: "SPELL_EFFECT_DISENCHANT - 分解",
    100: "SPELL_EFFECT_INEBRIATE - 醉酒",
    101: "SPELL_EFFECT_FEED_PET - 喂养宠物",
    102: "SPELL_EFFECT_DISMISS_PET - 解散宠物",
    103: "SPELL_EFFECT_REPUTATION - 声望",
    104: "SPELL_EFFECT_SUMMON_OBJECT_SLOT1 - 召唤物品栏位1",
    105: "SPELL_EFFECT_SUMMON_OBJECT_SLOT2 - 召唤物品栏位2",
    106: "SPELL_EFFECT_SUMMON_OBJECT_SLOT3 - 召唤物品栏位3",
    107: "SPELL_EFFECT_SUMMON_OBJECT_SLOT4 - 召唤物品栏位4",
    108: "SPELL_EFFECT_DISPEL_MECHANIC - 驱散机制",
    109: "SPELL_EFFECT_RESURRECT_PET - 复活宠物",
    110: "SPELL_EFFECT_DESTROY_ALL_TOTEMS - 摧毁所有图腾",
    111: "SPELL_EFFECT_DURABILITY_DAMAGE - 耐久度伤害",
    112: "SPELL_EFFECT_SUMMON_DEMON - 召唤恶魔",
    113: "SPELL_EFFECT_RESURRECT_NEW - 新的复活",
    114: "SPELL_EFFECT_ATTACK_ME - 攻击我",
    115: "SPELL_EFFECT_DURABILITY_DAMAGE_PCT - 耐久度百分比伤害",
    116: "SPELL_EFFECT_SKIN_PLAYER_CORPSE - 剥皮玩家尸体",
    117: "SPELL_EFFECT_SPIRIT_HEAL - 灵魂治疗",
    118: "SPELL_EFFECT_SKILL - 技能",
    119: "SPELL_EFFECT_APPLY_AREA_AURA_PET - 应用宠物区域光环",
    120: "SPELL_EFFECT_TELEPORT_GRAVEYARD - 传送到墓地",
    121: "SPELL_EFFECT_NORMALIZED_WEAPON_DMG - 标准化武器伤害",
    122: "SPELL_EFFECT_SERVER_SIDE - 服务器端效果",
    123: "SPELL_EFFECT_SEND_TAXI - 发送飞行坐骑",
    124: "SPELL_EFFECT_PULL_TOWARDS - 拉向",
    125: "SPELL_EFFECT_MODIFY_THREAT_PERCENT - 修改威胁百分比",
    126: "SPELL_EFFECT_STEAL_BENEFICIAL_BUFF - 偷取有益状态",
    127: "SPELL_EFFECT_PROSPECTING - 勘探",
    128: "SPELL_EFFECT_APPLY_AREA_AURA_FRIEND - 应用友方区域光环",
    129: "SPELL_EFFECT_APPLY_AREA_AURA_ENEMY - 应用敌方区域光环",
    130: "SPELL_EFFECT_REDIRECT_THREAT - 重定向威胁",
    131: "SPELL_EFFECT_PLAY_SOUND - 播放声音",
    132: "SPELL_EFFECT_PLAY_MUSIC - 播放音乐",
    133: "SPELL_EFFECT_UNLEARN_SPECIALIZATION - 遗忘专精",
    134: "SPELL_EFFECT_KILL_CREDIT2 - 击杀计数2",
    135: "SPELL_EFFECT_CALL_PET - 召唤宠物",
    136: "SPELL_EFFECT_HEAL_PCT - 百分比治疗",
    137: "SPELL_EFFECT_ENERGIZE_PCT - 百分比能量恢复",
    138: "SPELL_EFFECT_LEAP_BACK - 向后跳跃",
    139: "SPELL_EFFECT_CLEAR_QUEST - 清除任务",
    140: "SPELL_EFFECT_FORCE_CAST - 强制施法",
    141: "SPELL_EFFECT_FORCE_CAST_WITH_VALUE - 带值强制施法",
    142: "SPELL_EFFECT_TRIGGER_SPELL_WITH_VALUE - 带值触发法术",
    143: "SPELL_EFFECT_APPLY_AREA_AURA_OWNER - 应用所有者区域光环",
    144: "SPELL_EFFECT_KNOCK_BACK_DEST - 击退到目标点",
    145: "SPELL_EFFECT_PULL_TOWARDS_DEST - 拉向目标点",
    146: "SPELL_EFFECT_ACTIVATE_RUNE - 激活符文",
    147: "SPELL_EFFECT_QUEST_FAIL - 任务失败",
    148: "SPELL_EFFECT_TRIGGER_MISSILE_SPELL_WITH_VALUE - 带值触发飞弹法术",
    149: "SPELL_EFFECT_CHARGE_DEST - 冲锋到目标点",
    150: "SPELL_EFFECT_QUEST_START - 开始任务",
    151: "SPELL_EFFECT_TRIGGER_SPELL_2 - 触发法术2",
    152: "SPELL_EFFECT_SUMMON_RAF_FRIEND - 召唤推荐好友",
    153: "SPELL_EFFECT_CREATE_TAMED_PET - 创建已驯服宠物",
    154: "SPELL_EFFECT_DISCOVER_TAXI - 发现飞行点"
}

# 法术效果光环类型定义
SPELL_AURA_TYPES = {
    0: "SPELL_AURA_NONE - 无光环",
    1: "SPELL_AURA_BIND_SIGHT - 绑定视野",
    2: "SPELL_AURA_MOD_POSSESS - 控制",
    3: "SPELL_AURA_PERIODIC_DAMAGE - 周期伤害",
    4: "SPELL_AURA_DUMMY - 虚拟光环",
    5: "SPELL_AURA_MOD_CONFUSE - 混乱",
    6: "SPELL_AURA_MOD_CHARM - 魅惑",
    7: "SPELL_AURA_MOD_FEAR - 恐惧",
    8: "SPELL_AURA_PERIODIC_HEAL - 周期治疗",
    9: "SPELL_AURA_MOD_ATTACKSPEED - 攻击速度",
    10: "SPELL_AURA_MOD_THREAT - 威胁值",
    11: "SPELL_AURA_MOD_TAUNT - 嘲讽",
    12: "SPELL_AURA_MOD_STUN - 昏迷",
    13: "SPELL_AURA_MOD_DAMAGE_DONE - 伤害加成",
    14: "SPELL_AURA_MOD_DAMAGE_TAKEN - 受伤加成",
    15: "SPELL_AURA_DAMAGE_SHIELD - 伤害护盾",
    16: "SPELL_AURA_MOD_STEALTH - 潜行",
    17: "SPELL_AURA_MOD_STEALTH_DETECT - 侦测潜行",
    18: "SPELL_AURA_MOD_INVISIBILITY - 隐形",
    19: "SPELL_AURA_MOD_INVISIBILITY_DETECT - 侦测隐形",
    20: "SPELL_AURA_OBS_MOD_HEALTH - 生命值修改",
    21: "SPELL_AURA_OBS_MOD_POWER - 能量值修改",
    22: "SPELL_AURA_MOD_RESISTANCE - 抗性",
    23: "SPELL_AURA_PERIODIC_TRIGGER_SPELL - 周期触发法术",
    24: "SPELL_AURA_PERIODIC_ENERGIZE - 周期能量",
    25: "SPELL_AURA_MOD_PACIFY - 安抚",
    26: "SPELL_AURA_MOD_ROOT - 定身",
    27: "SPELL_AURA_MOD_SILENCE - 沉默",
    28: "SPELL_AURA_REFLECT_SPELLS - 法术反射",
    29: "SPELL_AURA_MOD_STAT - 属性修改",
    30: "SPELL_AURA_MOD_SKILL - 技能修改",
    31: "SPELL_AURA_MOD_INCREASE_SPEED - 增加速度",
    32: "SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED - 增加坐骑速度",
    33: "SPELL_AURA_MOD_DECREASE_SPEED - 降低速度",
    34: "SPELL_AURA_MOD_INCREASE_HEALTH - 增加生命值",
    35: "SPELL_AURA_MOD_INCREASE_ENERGY - 增加能量值",
    36: "SPELL_AURA_MOD_SHAPESHIFT - 变形",
    37: "SPELL_AURA_EFFECT_IMMUNITY - 效果免疫",
    38: "SPELL_AURA_STATE_IMMUNITY - 状态免疫",
    39: "SPELL_AURA_SCHOOL_IMMUNITY - 学派免疫",
    40: "SPELL_AURA_DAMAGE_IMMUNITY - 伤害免疫",
    41: "SPELL_AURA_DISPEL_IMMUNITY - 驱散免疫",
    42: "SPELL_AURA_PROC_TRIGGER_SPELL - 触发法术",
    43: "SPELL_AURA_PROC_TRIGGER_DAMAGE - 触发伤害",
    44: "SPELL_AURA_TRACK_CREATURES - 追踪生物",
    45: "SPELL_AURA_TRACK_RESOURCES - 追踪资源",
    46: "SPELL_AURA_MOD_PARRY_SKILL - 招架技能",
    47: "SPELL_AURA_MOD_PARRY_PERCENT - 招架几率",
    48: "SPELL_AURA_MOD_DODGE_SKILL - 无效果",
    49: "SPELL_AURA_MOD_DODGE_PERCENT - 闪避几率",
    50: "SPELL_AURA_MOD_BLOCK_SKILL - 格挡技能",
    51: "SPELL_AURA_MOD_BLOCK_PERCENT - 格挡几率",
    52: "SPELL_AURA_MOD_CRIT_PERCENT - 暴击几率",
    53: "SPELL_AURA_PERIODIC_LEECH - 周期吸取",
    54: "SPELL_AURA_MOD_HIT_CHANCE - 命中几率",
    55: "SPELL_AURA_MOD_SPELL_HIT_CHANCE - 法术命中几率",
    56: "SPELL_AURA_TRANSFORM - 变形",
    57: "SPELL_AURA_MOD_SPELL_CRIT_CHANCE - 法术暴击几率",
    58: "SPELL_AURA_MOD_INCREASE_SWIM_SPEED - 增加游泳速度",
    59: "SPELL_AURA_MOD_DAMAGE_DONE_CREATURE - 对生物伤害加成",
    60: "SPELL_AURA_MOD_PACIFY_SILENCE - 沉默安抚",
    61: "SPELL_AURA_MOD_SCALE - 体型缩放",
    62: "SPELL_AURA_PERIODIC_HEALTH_FUNNEL - 周期生命漏斗",
    63: "SPELL_AURA_PERIODIC_MANA_FUNNEL - 周期法力漏斗",
    64: "SPELL_AURA_PERIODIC_MANA_LEECH - 周期法力吸取",
    65: "SPELL_AURA_MOD_CASTING_SPEED_NOT_STACK - 施法速度(不叠加)",
    66: "SPELL_AURA_FEIGN_DEATH - 假死",
    67: "SPELL_AURA_MOD_DISARM - 缴械",
    68: "SPELL_AURA_MOD_STALKED - 被追踪",
    69: "SPELL_AURA_SCHOOL_ABSORB - 学派吸收",
    70: "SPELL_AURA_EXTRA_ATTACKS - 额外攻击",
    71: "SPELL_AURA_MOD_SPELL_CRIT_CHANCE_SCHOOL - 法术学派暴击几率",
    72: "SPELL_AURA_MOD_POWER_COST_SCHOOL_PCT - 法术学派能量消耗百分比",
    73: "SPELL_AURA_MOD_POWER_COST_SCHOOL - 法术学派能量消耗",
    74: "SPELL_AURA_REFLECT_SPELLS_SCHOOL - 反射法术学派",
    75: "SPELL_AURA_MOD_LANGUAGE - 语言",
    76: "SPELL_AURA_FAR_SIGHT - 远视",
    77: "SPELL_AURA_MECHANIC_IMMUNITY - 机制免疫",
    78: "SPELL_AURA_MOUNTED - 坐骑",
    79: "SPELL_AURA_MOD_DAMAGE_PERCENT_DONE - 伤害百分比",
    80: "SPELL_AURA_MOD_PERCENT_STAT - 属性百分比",
    81: "SPELL_AURA_SPLIT_DAMAGE_PCT - 伤害分摊百分比",
    82: "SPELL_AURA_WATER_BREATHING - 水下呼吸",
    83: "SPELL_AURA_MOD_BASE_RESISTANCE - 基础抗性",
    84: "SPELL_AURA_MOD_REGEN - 恢复速度",
    85: "SPELL_AURA_MOD_POWER_REGEN - 能量恢复速度",
    86: "SPELL_AURA_CHANNEL_DEATH_ITEM - 死亡物品引导",
    87: "SPELL_AURA_MOD_DAMAGE_PERCENT_TAKEN - 受伤百分比",
    88: "SPELL_AURA_MOD_HEALTH_REGEN_PERCENT - 生命恢复百分比",
    89: "SPELL_AURA_PERIODIC_DAMAGE_PERCENT - 周期伤害百分比",
    90: "SPELL_AURA_MOD_RESIST_CHANCE - 抗性几率",
    91: "SPELL_AURA_MOD_DETECT_RANGE - 侦测范围",
    92: "SPELL_AURA_PREVENTS_FLEEING - 防止逃跑",
    93: "SPELL_AURA_MOD_UNATTACKABLE - 不可攻击",
    94: "SPELL_AURA_INTERRUPT_REGEN - 打断恢复",
    95: "SPELL_AURA_GHOST - 灵魂",
    96: "SPELL_AURA_SPELL_MAGNET - 法术磁石",
    97: "SPELL_AURA_MANA_SHIELD - 法力护盾",
    98: "SPELL_AURA_MOD_SKILL_TALENT - 技能天赋",
    99: "SPELL_AURA_MOD_ATTACK_POWER - 攻击强度",
    100: "SPELL_AURA_AURAS_VISIBLE - 光环可见",
    # ... 更多光环类型
}

# 法术效果机制定义
SPELL_EFFECT_MECHANICS = {
    0: "MECHANIC_NONE - 无机制",
    1: "MECHANIC_CHARM - 魅",
    2: "MECHANIC_DISORIENTED - 迷惑",
    3: "MECHANIC_DISARM - 缴械",
    4: "MECHANIC_DISTRACT - 扰乱",
    5: "MECHANIC_FEAR - 恐惧",
    6: "MECHANIC_GRIP - 束缚",
    7: "MECHANIC_ROOT - 定身",
    8: "MECHANIC_SLOW_ATTACK - 减速攻击",
    9: "MECHANIC_SILENCE - 沉默",
    10: "MECHANIC_SLEEP - 睡眠",
    11: "MECHANIC_SNARE - 陷阱",
    12: "MECHANIC_STUN - 昏迷",
    13: "MECHANIC_FREEZE - 冰冻",
    14: "MECHANIC_KNOCKOUT - 击倒",
    15: "MECHANIC_BLEED - 流血",
    16: "MECHANIC_BANDAGE - 绷带",
    17: "MECHANIC_POLYMORPH - 变形",
    18: "MECHANIC_BANISH - 放逐",
    19: "MECHANIC_SHIELD - 护盾",
    20: "MECHANIC_SHACKLE - 束缚",
    21: "MECHANIC_MOUNT - 坐骑",
    22: "MECHANIC_INFECTED - 感染",
    23: "MECHANIC_TURN - 转化",
    24: "MECHANIC_HORROR - 恐慌",
    25: "MECHANIC_INVULNERABILITY - 无敌",
    26: "MECHANIC_INTERRUPT - 打断",
    27: "MECHANIC_DAZE - 眩晕",
    28: "MECHANIC_DISCOVERY - 发现",
    29: "MECHANIC_IMMUNE_SHIELD - 免疫护盾",
    30: "MECHANIC_SAPPED - 瘫痪"
}

# 法术学派定义
SPELL_SCHOOLS = {
    0: "SPELL_SCHOOL_NORMAL - 物理",
    1: "SPELL_SCHOOL_HOLY - 神圣",
    2: "SPELL_SCHOOL_FIRE - 火焰",
    3: "SPELL_SCHOOL_NATURE - 自然",
    4: "SPELL_SCHOOL_FROST - 冰霜",
    5: "SPELL_SCHOOL_SHADOW - 暗影",
    6: "SPELL_SCHOOL_ARCANE - 奥术"
}

# 法术伤害类型定义
SPELL_DAMAGE_CLASS = {
    0: "SPELL_DAMAGE_CLASS_NONE - 无",
    1: "SPELL_DAMAGE_CLASS_MAGIC - 魔法",
    2: "SPELL_DAMAGE_CLASS_MELEE - 近战",
    3: "SPELL_DAMAGE_CLASS_RANGED - 远程"
}

# 法术能量类型定义
SPELL_POWER_TYPE = {
    0: "POWER_MANA - 法力值",
    1: "POWER_RAGE - 怒气",
    2: "POWER_FOCUS - 集中值",
    3: "POWER_ENERGY - 能量",
    4: "POWER_HAPPINESS - 快乐度",
    5: "POWER_RUNE - 符文能量",
    6: "POWER_RUNIC_POWER - 符文能量"
}

# 法术族定义
SPELL_FAMILY = {
    0: "SPELLFAMILY_GENERIC - 通用",
    1: "SPELLFAMILY_UNK1 - 未知1",
    2: "SPELLFAMILY_MAGE - 法师",
    3: "SPELLFAMILY_WARRIOR - 战士", 
    4: "SPELLFAMILY_WARLOCK - 术士",
    5: "SPELLFAMILY_PRIEST - 牧师",
    6: "SPELLFAMILY_DRUID - 德鲁伊",
    7: "SPELLFAMILY_ROGUE - 潜行者",
    8: "SPELLFAMILY_HUNTER - 猎人",
    9: "SPELLFAMILY_PALADIN - 圣骑士",
    10: "SPELLFAMILY_SHAMAN - 萨满祭司",
    11: "SPELLFAMILY_UNK2 - 未知2",
    12: "SPELLFAMILY_UNK3 - 未知3"
}

# 法术驱散类型定义
SPELL_DISPEL_TYPE = {
    0: "DISPEL_NONE - 无",
    1: "DISPEL_MAGIC - 魔法",
    2: "DISPEL_CURSE - 诅咒",
    3: "DISPEL_DISEASE - 疾病",
    4: "DISPEL_POISON - 毒药",
    5: "DISPEL_STEALTH - 潜行",
    6: "DISPEL_INVISIBILITY - 隐形",
    7: "DISPEL_ALL - 所有",
    8: "DISPEL_SPE_NPC_ONLY - 仅NPC特殊",
    9: "DISPEL_ENRAGE - 激怒",
    10: "DISPEL_ZG_TICKET - ZG令牌"
}

# 法术机制类型定义
SPELL_MECHANIC = {
    0: "MECHANIC_NONE - 无",
    1: "MECHANIC_CHARM - 魅惑",
    2: "MECHANIC_DISORIENTED - 迷惑",
    3: "MECHANIC_DISARM - 缴械",
    4: "MECHANIC_DISTRACT - 扰乱",
    5: "MECHANIC_FEAR - 恐惧",
    6: "MECHANIC_GRIP - 束缚",
    7: "MECHANIC_ROOT - 定身",
    8: "MECHANIC_SLOW_ATTACK - 减速攻击",
    9: "MECHANIC_SILENCE - 沉默",
    10: "MECHANIC_SLEEP - 睡眠",
    11: "MECHANIC_SNARE - 陷阱",
    12: "MECHANIC_STUN - 昏迷",
    13: "MECHANIC_FREEZE - 冰冻",
    14: "MECHANIC_KNOCKOUT - 击倒",
    15: "MECHANIC_BLEED - 流血",
    16: "MECHANIC_BANDAGE - 绷带",
    17: "MECHANIC_POLYMORPH - 变形",
    18: "MECHANIC_BANISH - 放逐",
    19: "MECHANIC_SHIELD - 护盾",
    20: "MECHANIC_SHACKLE - 束缚",
    21: "MECHANIC_MOUNT - 坐骑",
    22: "MECHANIC_INFECTED - 感染",
    23: "MECHANIC_TURN - 转化",
    24: "MECHANIC_HORROR - 恐慌",
    25: "MECHANIC_INVULNERABILITY - 无敌",
    26: "MECHANIC_INTERRUPT - 打断",
    27: "MECHANIC_DAZE - 眩晕",
    28: "MECHANIC_DISCOVERY - 发现",
    29: "MECHANIC_IMMUNE_SHIELD - 免疫护盾",
    30: "MECHANIC_SAPPED - 瘫痪"
}

# 法术目标生物类型定义
SPELL_TARGET_CREATURE_TYPE = {
    0: "CREATURE_TYPE_BEAST - 野兽",
    1: "CREATURE_TYPE_DRAGONKIN - 龙类",
    2: "CREATURE_TYPE_DEMON - 恶魔",
    3: "CREATURE_TYPE_ELEMENTAL - 元素",
    4: "CREATURE_TYPE_GIANT - 巨人",
    5: "CREATURE_TYPE_UNDEAD - 亡灵",
    6: "CREATURE_TYPE_HUMANOID - 人型生物",
    7: "CREATURE_TYPE_CRITTER - 小动物",
    8: "CREATURE_TYPE_MECHANICAL - 机械",
    9: "CREATURE_TYPE_NOT_SPECIFIED - 未指定",
    10: "CREATURE_TYPE_TOTEM - 图腾",
    11: "CREATURE_TYPE_NON_COMBAT_PET - 非战斗宠物",
    12: "CREATURE_TYPE_GAS_CLOUD - 气体云"
}

# 法术防护类型定义
SPELL_PREVENTION_TYPE = {
    0: "SPELL_PREVENTION_TYPE_NONE - 无",
    1: "SPELL_PREVENTION_TYPE_SILENCE - 沉默",
    2: "SPELL_PREVENTION_TYPE_PACIFY - 安抚"
}

# 法术触发类型定义
SPELL_PROC_FLAGS = {
    0x00000001: "PROC_FLAG_KILLED - 被击杀时触发",
    0x00000002: "PROC_FLAG_KILL - 击杀目标时触发",
    0x00000004: "PROC_FLAG_DONE_MELEE_AUTO_ATTACK - 造成近战自动攻击时触发",
    0x00000008: "PROC_FLAG_TAKEN_MELEE_AUTO_ATTACK - 受到近战自动攻击时触发",
    0x00000010: "PROC_FLAG_DONE_SPELL_MELEE_DMG_CLASS - 造成近战法术伤害时触发",
    0x00000020: "PROC_FLAG_TAKEN_SPELL_MELEE_DMG_CLASS - 受到近战法术伤害时触发",
    0x00000040: "PROC_FLAG_DONE_RANGED_AUTO_ATTACK - 造成远程自动攻击时触发",
    0x00000080: "PROC_FLAG_TAKEN_RANGED_AUTO_ATTACK - 受到远程自动攻击时触发",
    0x00000100: "PROC_FLAG_DONE_SPELL_RANGED_DMG_CLASS - 造成远程法术伤害时触发",
    0x00000200: "PROC_FLAG_TAKEN_SPELL_RANGED_DMG_CLASS - 受到远程法术伤害时触发",
    0x00000400: "PROC_FLAG_DONE_SPELL_NONE_DMG_CLASS_POS - 造成正面非伤害法术时触发",
    0x00000800: "PROC_FLAG_TAKEN_SPELL_NONE_DMG_CLASS_POS - 受到正面非伤害法术时触发",
    0x00001000: "PROC_FLAG_DONE_SPELL_NONE_DMG_CLASS_NEG - 造成负面非伤害法术时触发",
    0x00002000: "PROC_FLAG_TAKEN_SPELL_NONE_DMG_CLASS_NEG - 受到负面非伤害法术时触发",
    0x00004000: "PROC_FLAG_DONE_SPELL_MAGIC_DMG_CLASS_POS - 造成正面魔法伤害时触发",
    0x00008000: "PROC_FLAG_TAKEN_SPELL_MAGIC_DMG_CLASS_POS - 受到正面魔法伤害时触发",
    0x00010000: "PROC_FLAG_DONE_SPELL_MAGIC_DMG_CLASS_NEG - 造成负面魔法伤害时触发",
    0x00020000: "PROC_FLAG_TAKEN_SPELL_MAGIC_DMG_CLASS_NEG - 受到负面魔法伤害时触发",
    0x00040000: "PROC_FLAG_DONE_PERIODIC - 造成周期性效果时触发",
    0x00080000: "PROC_FLAG_TAKEN_PERIODIC - 受到周期性效果时触发",
    0x00100000: "PROC_FLAG_TAKEN_DAMAGE - 受到伤害时触发",
    0x00200000: "PROC_FLAG_DONE_TRAP_ACTIVATION - 陷阱激活时触发",
    0x00400000: "PROC_FLAG_DONE_MAINHAND_ATTACK - 主手攻击时触发",
    0x00800000: "PROC_FLAG_DONE_OFFHAND_ATTACK - 副手攻击时触发",
    0x01000000: "PROC_FLAG_DEATH - 死亡时触发"
}

# 装备型定义
ITEM_CLASS = {
    0: "ITEM_CLASS_CONSUMABLE - 消耗品",
    1: "ITEM_CLASS_CONTAINER - 容器",
    2: "ITEM_CLASS_WEAPON - 武器",
    3: "ITEM_CLASS_GEM - 宝石",
    4: "ITEM_CLASS_ARMOR - 护甲",
    5: "ITEM_CLASS_REAGENT - 材料",
    6: "ITEM_CLASS_PROJECTILE - 弹药",
    7: "ITEM_CLASS_TRADE_GOODS - 商品",
    8: "ITEM_CLASS_GENERIC - 其他",
    9: "ITEM_CLASS_RECIPE - 配方",
    10: "ITEM_CLASS_MONEY - 货币",
    11: "ITEM_CLASS_QUIVER - 箭袋",
    12: "ITEM_CLASS_QUEST - 任务",
    13: "ITEM_CLASS_KEY - 钥匙",
    14: "ITEM_CLASS_PERMANENT - 永久",
    15: "ITEM_CLASS_MISC - 杂项"
}

# 武器子类型定义
ITEM_SUBCLASS_WEAPON = {
    0: "ITEM_SUBCLASS_WEAPON_AXE - 斧",
    1: "ITEM_SUBCLASS_WEAPON_AXE2 - 双手斧",
    2: "ITEM_SUBCLASS_WEAPON_BOW - 弓",
    3: "ITEM_SUBCLASS_WEAPON_GUN - 枪",
    4: "ITEM_SUBCLASS_WEAPON_MACE - 锤",
    5: "ITEM_SUBCLASS_WEAPON_MACE2 - 双手锤",
    6: "ITEM_SUBCLASS_WEAPON_POLEARM - 长柄武器",
    7: "ITEM_SUBCLASS_WEAPON_SWORD - 剑",
    8: "ITEM_SUBCLASS_WEAPON_SWORD2 - 双手剑",
    9: "ITEM_SUBCLASS_WEAPON_WARGLAIVE - 战刃",
    10: "ITEM_SUBCLASS_WEAPON_STAFF - 法杖",
    11: "ITEM_SUBCLASS_WEAPON_EXOTIC - 特殊",
    12: "ITEM_SUBCLASS_WEAPON_EXOTIC2 - 特殊2",
    13: "ITEM_SUBCLASS_WEAPON_FIST - 拳套",
    14: "ITEM_SUBCLASS_WEAPON_MISC - 其他",
    15: "ITEM_SUBCLASS_WEAPON_DAGGER - 匕首",
    16: "ITEM_SUBCLASS_WEAPON_THROWN - 投掷武器",
    17: "ITEM_SUBCLASS_WEAPON_SPEAR - 矛",
    18: "ITEM_SUBCLASS_WEAPON_CROSSBOW - 弩",
    19: "ITEM_SUBCLASS_WEAPON_WAND - 魔杖",
    20: "ITEM_SUBCLASS_WEAPON_FISHING_POLE - 鱼竿"
}

# 护甲子类型定义
ITEM_SUBCLASS_ARMOR = {
    0: "ITEM_SUBCLASS_ARMOR_MISC - 其他",
    1: "ITEM_SUBCLASS_ARMOR_CLOTH - 布甲",
    2: "ITEM_SUBCLASS_ARMOR_LEATHER - 皮甲",
    3: "ITEM_SUBCLASS_ARMOR_MAIL - 锁甲",
    4: "ITEM_SUBCLASS_ARMOR_PLATE - 板甲",
    5: "ITEM_SUBCLASS_ARMOR_BUCKLER - 小盾",
    6: "ITEM_SUBCLASS_ARMOR_SHIELD - 盾牌",
    7: "ITEM_SUBCLASS_ARMOR_LIBRAM - 圣契",
    8: "ITEM_SUBCLASS_ARMOR_IDOL - 神像",
    9: "ITEM_SUBCLASS_ARMOR_TOTEM - 图腾",
    10: "ITEM_SUBCLASS_ARMOR_SIGIL - 魔印"
}

# 装备栏位定义
INVENTORY_TYPE = {
    0: "INVTYPE_NON_EQUIP - 不可装备",
    1: "INVTYPE_HEAD - 头部",
    2: "INVTYPE_NECK - 颈部",
    3: "INVTYPE_SHOULDERS - 肩部",
    4: "INVTYPE_BODY - 衬衣",
    5: "INVTYPE_CHEST - 胸甲",
    6: "INVTYPE_WAIST - 腰部",
    7: "INVTYPE_LEGS - 腿部",
    8: "INVTYPE_FEET - 脚部",
    9: "INVTYPE_WRISTS - 手腕",
    10: "INVTYPE_HANDS - 手套",
    11: "INVTYPE_FINGER - 戒指",
    12: "INVTYPE_TRINKET - 饰品",
    13: "INVTYPE_WEAPON - 单手武器",
    14: "INVTYPE_SHIELD - 盾牌",
    15: "INVTYPE_RANGED - 远程武器",
    16: "INVTYPE_CLOAK - 披风",
    17: "INVTYPE_2HWEAPON - 双手武器",
    18: "INVTYPE_BAG - 背包",
    19: "INVTYPE_TABARD - 战袍",
    20: "INVTYPE_ROBE - 长袍",
    21: "INVTYPE_WEAPONMAINHAND - 主手武器",
    22: "INVTYPE_WEAPONOFFHAND - 副手武器",
    23: "INVTYPE_HOLDABLE - 副手物品",
    24: "INVTYPE_AMMO - 弹药",
    25: "INVTYPE_THROWN - 投掷武器",
    26: "INVTYPE_RANGEDRIGHT - 远程武器",
    27: "INVTYPE_QUIVER - 箭袋",
    28: "INVTYPE_RELIC - 圣物"
}

# 法术范围定义
SPELL_RANGE = {
    1: "SPELL_RANGE_SELF - 自身",
    2: "SPELL_RANGE_COMBAT_MELEE - 近战范围(5码)",
    3: "SPELL_RANGE_COMBAT_RANGED - 远程范围(30码)",
    4: "SPELL_RANGE_LONG - 远程范围(40码)",
    5: "SPELL_RANGE_ANYWHERE - 任意位置",
    6: "SPELL_RANGE_FRIENDS - 友方目标",
    7: "SPELL_RANGE_ENEMIES - 敌方目标",
    8: "SPELL_RANGE_ENTRY - 指定目标",
    9: "SPELL_RANGE_HOME - 家",
    10: "SPELL_RANGE_NONE - 无范围限制"
}

# 法术效果半径定义
SPELL_RADIUS = {
    7: "2码",
    8: "5码",
    9: "20码",
    10: "30码",
    11: "45码",
    12: "100码",
    13: "10码",
    14: "8码",
    15: "3码",
    16: "1码",
    17: "13码",
    18: "15码",
    19: "18码",
    20: "25码",
    21: "35码",
    22: "200码",
    23: "40码",
    24: "65码",
    25: "70码",
    26: "4码",
    27: "50码",
    28: "50000码",
    29: "6码",
    31: "80码"
}

# 法术效果目标定义
SPELL_EFFECT_TARGET = {
    1: "SPELL_EFFECT_TARGET_NONE - 无目标",
    2: "SPELL_EFFECT_TARGET_SELF - 自身",
    3: "SPELL_EFFECT_TARGET_PET - 宠物",
    4: "SPELL_EFFECT_TARGET_SINGLE_ENEMY - 单个敌人",
    5: "SPELL_EFFECT_TARGET_CHAIN_DAMAGE - 连锁伤害",
    6: "SPELL_EFFECT_TARGET_SINGLE_FRIEND - 单个友方",
    7: "SPELL_EFFECT_TARGET_CHAIN_HEAL - 连锁治疗",
    8: "SPELL_EFFECT_TARGET_AREAEFFECT_PARTY - 队伍范围",
    9: "SPELL_EFFECT_TARGET_AREAEFFECT_ENEMY - 敌方范围",
    10: "SPELL_EFFECT_TARGET_AREAEFFECT_FRIEND - 友方范围",
    11: "SPELL_EFFECT_TARGET_AROUND_CASTER - 施法者周围",
    12: "SPELL_EFFECT_TARGET_SELECTED_FRIEND - 选中的友方",
    13: "SPELL_EFFECT_TARGET_AROUND_ENTRY - 指定目标周围",
    14: "SPELL_EFFECT_TARGET_SELECTED_GAMEOBJECT - 选中的游戏对象",
    15: "SPELL_EFFECT_TARGET_INFRONT - 前方锥形",
    16: "SPELL_EFFECT_TARGET_BEHIND - 身后",
    17: "SPELL_EFFECT_TARGET_RIGHT - 右侧",
    18: "SPELL_EFFECT_TARGET_LEFT - 左侧",
    19: "SPELL_EFFECT_TARGET_MASTER - 主人",
    20: "SPELL_EFFECT_TARGET_ALL_PARTY - 所有队伍成员",
    21: "SPELL_EFFECT_TARGET_ALL_RAID - 所有团队成员",
    22: "SPELL_EFFECT_TARGET_SELF_FISHING - 自身钓鱼",
    23: "SPELL_EFFECT_TARGET_CHAIN_HEAL_2 - 连锁治疗2",
    24: "SPELL_EFFECT_TARGET_IN_FRONT_OF_CASTER - 施法者前方",
    25: "SPELL_EFFECT_TARGET_DUEL_VS_PLAYER - 决斗玩家",
    26: "SPELL_EFFECT_TARGET_GAMEOBJECT_ITEM - 物品",
    27: "SPELL_EFFECT_TARGET_PET_MASTER - 宠物主人",
    28: "SPELL_EFFECT_TARGET_PULL_TOWARDS - 拉向",
    29: "SPELL_EFFECT_TARGET_PUSH_AWAY - 推开",
    30: "SPELL_EFFECT_TARGET_CIRCLE_AREA - 圆形范围"
}

# 法术持续时间定义
SPELL_DURATION = {
    1: "DURATION_MAX_10_SEC - 最大10秒",
    2: "DURATION_BMAX_30_SEC - 基础最大30秒",
    3: "DURATION_MAX_60_SEC - 最大60秒",
    4: "DURATION_MAX_120_SEC - 最大120秒", 
    5: "DURATION_MAX_300_SEC - 最大300秒",
    6: "DURATION_MAX_600_SEC - 最大600秒",
    7: "DURATION_BMAX_5_SEC_1 - 基础最大5秒",
    8: "DURATION_MAX_15_SEC - 最大15秒",
    9: "DURATION_MAX_30_SEC - 最大30秒",
    10: "DURATION_BMAX_60_SEC - 基础最大60秒",
    11: "DURATION_BPMAX_15_SEC - 基础最大15秒+等级加成",
    12: "DURATION_BPMAX_40_SEC_1 - 基础最大40秒+等级加成",
    13: "DURATION_BPMAX_80_SEC_1 - 基础最大80秒+等级加成",
    14: "DURATION_BPMAX_3_HRS - 基础最大3小时+等级成",
    15: "DURATION_BPMAX_7_HRS - 基础最大7小时+等级加成",
    16: "DURATION_MAX_230_MIN - 最大230分钟",
    17: "DURATION_BPMAX_7_SEC - 基础最大7秒+等级加成",
    18: "DURATION_MAX_20_SEC - 最大20秒",
    19: "DURATION_BPMAX_40_SEC_2 - 基础最大40秒+等级加成",
    20: "DURATION_BPMAX_80_SEC_2 - 基础最大80秒+等级加成",
    21: "DURATION_MAX_INFINITY - 无限持续",
    22: "DURATION_MAX_45_SEC - 最大45秒",
    23: "DURATION_MAX_90_SEC - 最大90秒",
    24: "DURATION_MAX_160_SEC - 最大160秒",
    25: "DURATION_MAX_180_SEC - 最大180秒",
    26: "DURATION_MAX_240_SEC - 最大240秒",
    27: "DURATION_MAX_3_SEC - 最大3秒",
    28: "DURATION_MAX_5_SEC - 最大5秒",
    29: "DURATION_MAX_12_SEC - 最大12秒",
    30: "DURATION_MAX_30_MIN - 最大30分钟",
    31: "DURATION_MAX_8_SEC - 最大8秒",
    32: "DURATION_MAX_6_SEC - 最大6秒",
    35: "DURATION_MAX_4_SEC - 最大4秒",
    36: "DURATION_MAX_1_SEC - 最大1秒",
    37: "DURATION_MAX_1_MSEC - 最大1毫秒",
    38: "DURATION_MAX_11_SEC - 最大11秒",
    39: "DURATION_MAX_2_SEC - 最大2秒",
    40: "DURATION_MAX_20_MIN - 最大20分钟",
    41: "DURATION_MAX_6_MIN - 最6分钟",
    42: "DURATION_MAX_60_MIN - 最大60分钟",
    62: "DURATION_MAX_75_SEC - 最大75秒",
    63: "DURATION_MAX_25_SEC - 最大25秒",
    64: "DURATION_MAX_40_SEC - 最大40秒",
    65: "DURATION_MAX_1_5_SEC - 最大1.5秒",
    66: "DURATION_MAX_2_5_SEC - 最大2.5秒",
    85: "DURATION_MAX_18_SEC - 最大18秒",
    86: "DURATION_MAX_21_SEC - 最大21秒",
    105: "DURATION_MAX_9_SEC - 最大9秒",
    106: "DURATION_MAX_24_SEC - 最大24秒",
    125: "DURATION_MAX_35_SEC - 最大35秒",
    145: "DURATION_MAX_45_MIN - 最大45分钟",
    165: "DURATION_MAX_7_SEC - 最大7秒",
    185: "DURATION_BMAX_21_SEC - 基础最大21秒",
    186: "DURATION_BMAX_22_SEC - 基础最大22秒",
    187: "DURATION_BMAX_5_SEC_2 - 基础最大5秒",
    205: "DURATION_MAX_27_SEC - 最大27秒",
    225: "DURATION_MAX_7_DAYS - 最大7天",
    245: "DURATION_MAX_50_SEC - 最大50秒",
    265: "DURATION_MAX_55_SEC - 最大55秒",
    285: "DURATION_BMAX_6_SEC_1 - 基础最大6秒",
    305: "DURATION_MAX_14_SEC - 最大14秒",
    325: "DURATION_MAX_36_SEC - 最大36秒",
    326: "DURATION_MAX_44_SEC - 最大44秒",
    327: "DURATION_MAX_500_MSEC - 最大500毫秒",
    328: "DURATION_MAX_250_MSEC - 最大250毫秒",
    347: "DURATION_MAX_15_MIN - 最大15分钟",
    367: "DURATION_MAX_2_HRS - 最大2小时",
    387: "DURATION_MAX_16_SEC - 最大16秒",
    407: "DURATION_MAX_100_MSEC - 最大100毫秒",
    427: "DURATION_BPMAX_10_MIN - 基础最大10分钟+等级加成",
    447: "DURATION_BMAX_6_SEC_2 - 基础最大6秒",
    467: "DURATION_MAX_22_SEC - 最大22秒",
    468: "DURATION_MAX_26_SEC - 最大26秒",
    487: "DURATION_MAX_1_7_SEC - 最大1.7秒",
    507: "DURATION_MAX_1_1_SEC_1 - 最大1.1秒",
    508: "DURATION_MAX_1_1_SEC_2 - 最大1.1秒",
    527: "DURATION_MAX_4_HRS - 最大4小时",
    547: "DURATION_MAX_90_MIN - 最大90分钟",
    548: "DURATION_MAX_3_HRS - 最大3小时",
    549: "DURATION_MAX_3_8_SEC - 最大3.8秒",
    550: "DURATION_MAX_24_8_DAYS - 最大24.8天",
    551: "DURATION_MAX_3_5_SEC - 最大3.5秒",
    552: "DURATION_MAX_210_SEC - 最大210秒",
    553: "DURATION_BMAX_16_SEC - 基础最大16秒",
    554: "DURATION_MAX_155_SEC - 最大155秒",
    555: "DURATION_MAX_4_5_SEC - 最大4.5秒",
    556: "DURATION_MAX_28_SEC - 最大28秒",
    557: "DURATION_MAX_165_SEC - 最大165秒",
    558: "DURATION_MAX_114_SEC - 最大114秒",
    559: "DURATION_MAX_53_SEC - 最大53秒",
    560: "DURATION_MAX_299_SEC - 最大299秒",
    561: "DURATION_MAX_55_MIN - 最大55分钟",
    562: "DURATION_MAX_150_SEC - 最大150秒",
    563: "DURATION_MAX_20_5_SEC - 最大20.5秒",
    564: "DURATION_MAX_13_SEC - 最大13秒",
    565: "DURATION_MAX_70_SEC - 最大70秒",
    566: "DURATION_MAX_0_SEC - 最大0秒",
    567: "DURATION_MAX_135_SEC - 最大135秒",
    568: "DURATION_MAX_1250_MSEC - 最大1250毫秒",
    569: "DURATION_MAX_280_SEC - 最大280秒",
    570: "DURATION_MAX_32_SEC - 最大32秒",
    571: "DURATION_MAX_5_5_SEC - 最大5.5秒",
    572: "DURATION_MAX_100_SEC - 最大100秒",
    573: "DURATION_MAX_9999_MSEC - 最大9999毫秒",
    574: "DURATION_MAX_200_MSEC - 最大200毫秒",
    575: "DURATION_MAX_17_SEC - 最大17秒",
    576: "DURATION_MAX_12_HRS - 最大12小时",
    580: "DURATION_MAX_18_HRS - 最大18小时"
}

# 法术施法时间定义
SPELL_CAST_TIME = {
    1: "SPELL_CAST_TIME_INSTANT - 瞬发 (0毫秒)",
    2: "SPELL_CAST_TIME_250MS - 250毫秒",
    3: "SPELL_CAST_TIME_500MS - 500毫秒",
    4: "SPELL_CAST_TIME_1000MS - 1000毫秒",
    5: "SPELL_CAST_TIME_2000MS - 2000毫秒",
    6: "SPELL_CAST_TIME_5000MS - 5000毫秒",
    7: "SPELL_CAST_TIME_10000MS - 10000毫秒",
    8: "SPELL_CAST_TIME_20000MS - 20000毫秒",
    9: "SPELL_CAST_TIME_30000MS - 30000毫秒",
    10: "SPELL_CAST_TIME_1000MS_SCALING - 1000毫秒(每级-100,最小500)",
    11: "SPELL_CAST_TIME_2000MS_SCALING - 2000毫秒(每级-100,最小1000)",
    12: "SPELL_CAST_TIME_5000MS_SCALING - 5000毫秒(每级-100,最小2500)",
    13: "SPELL_CAST_TIME_30000MS_SCALING - 30000毫秒(每级-1000,最小10000)",
    14: "SPELL_CAST_TIME_3000MS - 3000毫秒",
    15: "SPELL_CAST_TIME_4000MS - 4000毫秒",
    16: "SPELL_CAST_TIME_1500MS - 1500毫秒",
    18: "SPELL_CAST_TIME_NEGATIVE - -1000000毫秒",
    19: "SPELL_CAST_TIME_2500MS - 2500毫秒",
    20: "SPELL_CAST_TIME_2500MS_2 - 2500毫秒",
    21: "SPELL_CAST_TIME_2600MS - 2600毫秒",
    22: "SPELL_CAST_TIME_3500MS - 3500毫秒",
    23: "SPELL_CAST_TIME_1800MS - 1800毫秒",
    70: "SPELL_CAST_TIME_300000MS - 300000毫秒",
    90: "SPELL_CAST_TIME_1700MS - 1700毫秒",
    91: "SPELL_CAST_TIME_2800MS - 2800毫秒",
    170: "SPELL_CAST_TIME_8000MS - 8000毫秒",
    171: "SPELL_CAST_TIME_6000MS - 6000毫秒",
    192: "SPELL_CAST_TIME_15000MS - 15000毫秒",
    193: "SPELL_CAST_TIME_12000MS - 12000毫秒",
    195: "SPELL_CAST_TIME_1100MS - 1100毫秒",
    196: "SPELL_CAST_TIME_750MS - 750毫秒",
    197: "SPELL_CAST_TIME_850MS - 850毫秒",
    198: "SPELL_CAST_TIME_900MS - 900毫秒",
    199: "SPELL_CAST_TIME_333MS - 333毫秒"
}

# 法术目标类型定义
SPELL_TARGET_TYPE = {
    0: "TARGET_TYPE_NONE - 无目标",
    1: "TARGET_TYPE_UNIT - 单位",
    2: "TARGET_TYPE_UNIT_DEST - 单位位置",
    3: "TARGET_TYPE_DEST - 位置",
    4: "TARGET_TYPE_UNIT_CONE - 锥形范围",
    5: "TARGET_TYPE_UNIT_AREA - 区域",
    6: "TARGET_TYPE_DEST_AREA - 目标区域",
    7: "TARGET_TYPE_CHANNEL - 引导目标",
    8: "TARGET_TYPE_DEST_CHANNEL - 引导位置",
    9: "TARGET_TYPE_TARGET_LINE - 直线范围",
    10: "TARGET_TYPE_DEST_LINE - 目标直线"
}

# 添加法术目标定义
SPELL_IMPLICIT_TARGETS = {
    0: "TARGET_NONE - 无目标",
    1: "TARGET_UNIT_CASTER - 施法者",
    2: "TARGET_UNIT_ENEMY_NEAR_CASTER - 施法者附近的敌人",
    3: "TARGET_UNIT_FRIEND_NEAR_CASTER - 施法者附近的友方",
    4: "TARGET_UNIT_NEAR_CASTER - 施法者附近的单位",
    5: "TARGET_UNIT_CASTER_PET - 施法者的宠物",
    6: "TARGET_UNIT_ENEMY - 敌方单位",
    7: "TARGET_ENUM_UNITS_SCRIPT_AOE_AT_SRC_LOC - 源位置的脚本AOE单位",
    8: "TARGET_ENUM_UNITS_SCRIPT_AOE_AT_DEST_LOC - 目标位置的脚本AOE单位",
    9: "TARGET_LOCATION_CASTER_HOME_BIND - 施法者炉石位置",
    10: "TARGET_LOCATION_CASTER_DIVINE_BIND_NYI - 施法者神圣绑定位置",
    11: "TARGET_PLAYER_NYI - 玩家(未实现)",
    12: "TARGET_PLAYER_NEAR_CASTER_NYI - 施法附近的玩家(未实现)",
    13: "TARGET_PLAYER_ENEMY_NYI - 敌对玩家(未实现)",
    14: "TARGET_PLAYER_FRIEND_NYI - 友方玩家(未实现)",
    15: "TARGET_ENUM_UNITS_ENEMY_AOE_AT_SRC_LOC - 源位置的敌方AOE单位",
    16: "TARGET_ENUM_UNITS_ENEMY_AOE_AT_DEST_LOC - 目标位置的敌方AOE单位",
    17: "TARGET_LOCATION_DATABASE - 数据库中的位置",
    18: "TARGET_LOCATION_CASTER_DEST - 施法者目标位置",
    19: "TARGET_UNK_19 - 未知19",
    20: "TARGET_ENUM_UNITS_PARTY_WITHIN_CASTER_RANGE - 施法者范围内的队伍单位",
    21: "TARGET_UNIT_FRIEND - 友方单位",
    22: "TARGET_LOCATION_CASTER_SRC - 施法者源位置",
    23: "TARGET_GAMEOBJECT - 游戏对象",
    24: "TARGET_ENUM_UNITS_ENEMY_IN_CONE_24 - 锥形范围内的敌方单位",
    25: "TARGET_UNIT - 单位",
    26: "TARGET_LOCKED - 锁定目标",
    27: "TARGET_UNIT_CASTER_MASTER - 施法者的主人",
    28: "TARGET_ENUM_UNITS_ENEMY_AOE_AT_DYNOBJ_LOC - 动态对象位置的敌方AOE单位",
    29: "TARGET_ENUM_UNITS_FRIEND_AOE_AT_DYNOBJ_LOC - 动态对象位置的友方AOE单位",
    30: "TARGET_ENUM_UNITS_FRIEND_AOE_AT_SRC_LOC - 源位置的友方AOE单位",
    31: "TARGET_ENUM_UNITS_FRIEND_AOE_AT_DEST_LOC - 目标位置的友方AOE单位",
    32: "TARGET_LOCATION_UNIT_MINION_POSITION - 随从单位位置",
    33: "TARGET_ENUM_UNITS_PARTY_AOE_AT_SRC_LOC - 源位置的队伍AOE单位",
    34: "TARGET_ENUM_UNITS_PARTY_AOE_AT_DEST_LOC - 目标位置的队伍AOE单位",
    35: "TARGET_UNIT_PARTY - 队伍单位",
    36: "TARGET_ENUM_UNITS_ENEMY_WITHIN_CASTER_RANGE - 施法者范围内的敌方单位",
    37: "TARGET_UNIT_FRIEND_AND_PARTY - 友方和队伍单位",
    38: "TARGET_UNIT_SCRIPT_NEAR_CASTER - 施法者附近的脚本单位",
    39: "TARGET_LOCATION_CASTER_FISHING_SPOT - 施法者钓鱼点",
    40: "TARGET_GAMEOBJECT_SCRIPT_NEAR_CASTER - 施法者附近的脚本游戏对象",
    41: "TARGET_LOCATION_CASTER_FRONT_RIGHT - 施法者前右方",
    42: "TARGET_LOCATION_CASTER_BACK_RIGHT - 施法者后右方",
    43: "TARGET_LOCATION_CASTER_BACK_LEFT - 施法者后左方",
    44: "TARGET_LOCATION_CASTER_FRONT_LEFT - 施法者前左方",
    45: "TARGET_UNIT_FRIEND_CHAIN_HEAL - 友方连锁治疗目标",
    46: "TARGET_LOCATION_SCRIPT_NEAR_CASTER - 施法者附近的脚本位置",
    47: "TARGET_LOCATION_CASTER_FRONT - 施法者前方",
    48: "TARGET_LOCATION_CASTER_BACK - 施法者后方",
    49: "TARGET_LOCATION_CASTER_LEFT - 施法者左方",
    50: "TARGET_LOCATION_CASTER_RIGHT - 施法者右方",
    51: "TARGET_ENUM_GAMEOBJECTS_SCRIPT_AOE_AT_SRC_LOC - 源位置的脚本AOE游戏对象",
    52: "TARGET_ENUM_GAMEOBJECTS_SCRIPT_AOE_AT_DEST_LOC - 目标位置的脚本AOE游戏对象",
    53: "TARGET_LOCATION_CASTER_TARGET_POSITION - 施法者目标的位置",
    54: "TARGET_ENUM_UNITS_ENEMY_IN_CONE_54 - 锥形范围内的敌方单位54",
    55: "TARGET_LOCATION_CASTER_FRONT_LEAP - 施法者前方跳跃位置",
    56: "TARGET_ENUM_UNITS_RAID_WITHIN_CASTER_RANGE - 施法者范围内的团队单位",
    57: "TARGET_UNIT_RAID - 团队单位",
    58: "TARGET_UNIT_RAID_NEAR_CASTER - 施法者附近的团队单位",
    59: "TARGET_ENUM_UNITS_FRIEND_IN_CONE - 锥形范围内的友方单位",
    60: "TARGET_ENUM_UNITS_SCRIPT_IN_CONE_60 - 锥形范围内的脚本单位60",
    61: "TARGET_UNIT_RAID_AND_CLASS - 团队和职业单位",
    62: "TARGET_PLAYER_RAID_NYI - 团队玩家(未实现)",
    63: "TARGET_LOCATION_UNIT_POSITION - 单位位置"
}

# 法术光环状态定义
SPELL_AURA_STATE = {
    1: "AURA_STATE_DEFENSE - 防御姿态",
    2: "AURA_STATE_HEALTHLESS_20_PERCENT - 生命值低于20%",
    3: "AURA_STATE_BERSERKING - 狂暴",
    4: "AURA_STATE_FROZEN - 冰冻",
    5: "AURA_STATE_JUDGEMENT - 审判",
    6: "AURA_STATE_HUNTER_PARRY - 猎人招架",
    7: "AURA_STATE_WARRIOR_VICTORY_RUSH - 战士胜利冲锋",
    8: "AURA_STATE_HUNTER_CRIT_STRIKE - 猎人暴击",
    9: "AURA_STATE_CRIT - 暴击",
    10: "AURA_STATE_FAERIE_FIRE - 精灵之火",
    11: "AURA_STATE_HEALTHLESS_35_PERCENT - 生命值低于35%",
    12: "AURA_STATE_CONFLAGRATE - 燃烧",
    13: "AURA_STATE_SWIFTMEND - 迅捷治愈",
    14: "AURA_STATE_DEADLY_POISON - 致命毒药",
    15: "AURA_STATE_ENRAGE - 激怒",
    16: "AURA_STATE_BLEEDING - 流血",
    17: "AURA_STATE_DARK_FORCE - 黑暗之力",
    18: "AURA_STATE_FORBEARANCE - 自律",
    19: "AURA_STATE_WEAKENED_SOUL - 虚弱灵魂",
    20: "AURA_STATE_HYPOTHERMIA - 体温过低"
}

# 添加自定义标志位定义
SPELL_CUSTOM_FLAGS = {
    0x000: "SPELL_CUSTOM_NONE - 无自定义标志",
    0x001: "SPELL_CUSTOM_ALLOW_STACK_BETWEEN_CASTER - 允许不同施法者的效果叠加(例如'吸取灵魂')",
    0x002: "SPELL_CUSTOM_NEGATIVE - 负面效果",
    0x004: "SPELL_CUSTOM_POSITIVE - 正面效果",
    0x008: "SPELL_CUSTOM_CHAN_NO_DIST_LIMIT - 引导无距离限制",
    0x010: "SPELL_CUSTOM_FIXED_DAMAGE - 固定伤害(不受伤害/治疗加成影响)",
    0x020: "SPELL_CUSTOM_IGNORE_ARMOR - 无视护甲",
    0x040: "SPELL_CUSTOM_BEHIND_TARGET - 需要在目标背后施放",
    0x080: "SPELL_CUSTOM_FACE_TARGET - 需要在目标正面施放",
    0x100: "SPELL_CUSTOM_SINGLE_TARGET_AURA - 光环同时只能作用于一个目标",
    0x200: "SPELL_CUSTOM_AURA_APPLY_BREAKS_STEALTH - 光环应用时会打破潜行",
    0x400: "SPELL_CUSTOM_NOT_REMOVED_ON_EVADE - 生物逃跑时光环不会移除",
    0x800: "SPELL_CUSTOM_SEND_CHANNEL_VISUAL - 周期性发送引导法术视觉特效",
    0x1000: "SPELL_CUSTOM_SEPARATE_AURA_PER_CASTER - 每个施法者有独立的光环槽位,而不是替换其他人的"
}

