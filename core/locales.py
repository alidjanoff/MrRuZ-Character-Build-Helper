"""
locales.py — Multilingual text definitions for MuRuZ Character Build Helper.
Supported: English (en), Russian (ru), Azerbaijani (az).
"""

TEXTS = {
    "en": {
        "app_title": "⚔  MuRuZ Character Build Helper  ⚔",
        "app_sub": "Intelligent stat optimizer  ·  Formula-driven recommendations",
        "char_class": "CHARACTER CLASS",
        "prog": "PROGRESSION",
        "rst": "Reset Count",
        "lvl": "Current Level",
        "curr_stats": "CURRENT STATS",
        "rem_pts": "Remaining Pts",
        "vit_opt": "Invest in Vitality (VIT)?\n(Uncheck if gear gives enough HP)",
        "calc_btn": "⚡  Calculate Build",
        "calc_loading": "Calculating...",
        "recs": "BUILD RECOMMENDATIONS",
        "placeholder": ("\n\n   Select your class and enter stats,\n"
                        "   then click  ⚡ Calculate Build\n"
                        "   to see optimized recommendations.\n"),
        "analysis": "Analysis & Reasoning",
        
        "err_num": "Please enter a valid number for {name}.",
        "err_lvl": "Level must be between 1 and 400.",
        "err_rst": "Reset count cannot be negative.",
        "err_rem": "Remaining points cannot be negative.",
        "err_base": "{stat} cannot be less than {base}.",
        "err_miss": "You have {form:,} points but only {act:,} accounted for. Missing {diff:,} points.",
        "warn_title": "Validation Warning",
        "warn_msg": "{err}\n\nBuilds will still be generated.",
        
        "info_pts": "Formula points: {pts:,}",
        
        "farm_lbl": "🌾 FARM BUILD",
        "pve_lbl": "🛡️ PvE BUILD",
        "pvp_lbl": "⚔️ PvP BUILD",
        "farm_focus": "Fast killing speed · AoE efficiency · Sustain",
        "pve_focus": "Balanced damage + survivability · Boss fights",
        "pvp_focus": "Burst damage · Accuracy · Defense",
        
        "exp_total": "Total distributable points: {pts:,}",
        "exp_form": "  Formula: Lvl {lvl} × {ppl} pts/lvl + {rst} resets × 350 pts = {form:,}",
        "exp_bonus": "  + {bonus:,} bonus points (MMA / quests / events)",
        "exp_alloc": "Allocation breakdown:",
        "exp_pct": "% of points",
        "exp_der": "Key derived stats:",
        "der_dmg": "Avg Damage:",
        "der_combo": "Combo Damage:",
        "der_spd": "Attack Speed:",
        "der_def": "Defense:",
        "der_hp": "HP (from VIT):",
        "der_sd": "Shield Defense (SD):",
        "der_skill": "Skill Power:",
        "der_pvm_ar": "PvM Attack Rate:",
        "der_pvm_dr": "PvM Defense Rate:",
        "der_pvp_ar": "PvP Attack Rate:",
        "der_pvp_dr": "PvP Defense Rate:",
        "exp_rsn": "Reasoning:",
        
        "r_vit_skip": "• VIT investment skipped as requested (rely on gear for HP).",
        "r_f_prim": "• Primary damage scales with {stat}.",
        "r_f_spd": "• Attack Speed = {form} — higher AGI = faster kills.",
        "r_f_aoe": "• Skill% boosts AoE damage → efficient multi-target farming.",
        "r_f_vit": "• VIT kept moderate — potions handle sustain.",
        "r_f_high": "• {stat} received the most points ({pct}%) for best damage × speed.",
        
        "r_e_bal": "• Balanced between damage ({stat}) and survival (VIT/AGI).",
        "r_e_def": "• Defense = {form} — AGI reduces boss damage.",
        "r_e_vit": "• Higher VIT = more HP → survive powerful boss attacks.",
        "r_e_skill": "• Skill% still important for clearing dungeon adds.",
        "r_e_high": "• {stat} received the most points ({pct}%) for damage-to-tankiness ratio.",
        
        "r_p_brst": "• Burst damage from {stat} is essential to kill fast.",
        "r_p_ar": "• PvP Attack Rate heavily scales with AGI → must hit opponent.",
        "r_p_dr": "• PvP Defense Rate (AGI) helps dodge incoming hits.",
        "r_p_sd": "• SD = (all stats)×1.2 + Lvl²/30 → balanced stats help.",
        "r_p_high": "• {stat} received the most points ({pct}%) for max PvP effectiveness."
    },
    "ru": {
        "app_title": "⚔  MuRuZ Character Build Helper  ⚔",
        "app_sub": "Умный оптимизатор статов  ·  Рекомендации на основе формул",
        "char_class": "КЛАСС ПЕРСОНАЖА",
        "prog": "ПРОГРЕСС",
        "rst": "Количество ресетов",
        "lvl": "Текущий уровень",
        "curr_stats": "ТЕКУЩИЕ СТАТЫ",
        "rem_pts": "Осталось очков",
        "vit_opt": "Качать Vitality (VIT)?\n(Выключите, если хватает HP от сета)",
        "calc_btn": "⚡  Рассчитать билд",
        "calc_loading": "Расчет...",
        "recs": "РЕКОМЕНДОВАННЫЕ БИЛДЫ",
        "placeholder": ("\n\n   Выберите класс и введите статы,\n"
                        "   затем нажмите  ⚡ Рассчитать билд,\n"
                        "   чтобы увидеть оптимизированные билды.\n"),
        "analysis": "Анализ и пояснение",
        
        "err_num": "Пожалуйста, введите корректное число для {name}.",
        "err_lvl": "Уровень должен быть от 1 до 400.",
        "err_rst": "Количество ресетов не может быть отрицательным.",
        "err_rem": "Остаток очков не может быть отрицательным.",
        "err_base": "{stat} не может быть меньше {base}.",
        "err_miss": "Итого очков {form:,}, но введено лишь {act:,}. Не хватает {diff:,} очков.",
        "warn_title": "Предупреждение",
        "warn_msg": "{err}\n\nБилды все равно будут сгенерированы.",
        
        "info_pts": "Очки по формуле: {pts:,}",
        
        "farm_lbl": "🌾 FARM (ФАРМ) БИЛД",
        "pve_lbl": "🛡️ PvE (БОССЫ) БИЛД",
        "pvp_lbl": "⚔️ PvP (ИГРОКИ) БИЛД",
        "farm_focus": "Быстрое убийство мобов · Массовый урон · Выживаемость",
        "pve_focus": "Баланс урона и выживаемости · Походы на боссов",
        "pvp_focus": "Взрывной урон · Меткость · Защита",
        
        "exp_total": "Всего очков для распределения: {pts:,}",
        "exp_form": "  Формула: Ур {lvl} × {ppl} очк/ур + {rst} рес. × 350 очк = {form:,}",
        "exp_bonus": "  + {bonus:,} бонусных очков (MMA / квесты / эвенты)",
        "exp_alloc": "Распределение очков:",
        "exp_pct": "% от очков",
        "exp_der": "Ключевые производные статы:",
        "der_dmg": "Средний урон:",
        "der_combo": "Урон от комбо:",
        "der_spd": "Скорость атаки:",
        "der_def": "Защита (Defense):",
        "der_hp": "HP (от VIT):",
        "der_sd": "Защита щита (SD):",
        "der_skill": "Сила скилла (%):",
        "der_pvm_ar": "PvM Attack Rate:",
        "der_pvm_dr": "PvM Defense Rate:",
        "der_pvp_ar": "PvP Attack Rate:",
        "der_pvp_dr": "PvP Defense Rate:",
        "exp_rsn": "Пояснение:",
        
        "r_vit_skip": "• Прокачка VIT отключена, предполагается наличие HP с вещей.",
        "r_f_prim": "• Основной урон масштабируется от {stat}.",
        "r_f_spd": "• Скорость атак = {form} — больше AGI = быстрее убийства.",
        "r_f_aoe": "• Skill% увеличивает массовый урон → эффективный фарм.",
        "r_f_vit": "• VIT на базовом уровне — для выживания используются банки.",
        "r_f_high": "• {stat} получает больше всего очков ({pct}%) (идеально для скорости и урона).",
        
        "r_e_bal": "• Баланс между уроном ({stat}) и выживанием (VIT/AGI).",
        "r_e_def": "• Защита = {form} — AGI снижает получаемый от боссов урон.",
        "r_e_vit": "• Больше VIT = больше HP → переживаем сильные удары босса.",
        "r_e_skill": "• Skill% всё ещё важен для зачистки мелких мобов.",
        "r_e_high": "• В {stat} вложено {pct}% очков для баланса живучести и урона.",
        
        "r_p_brst": "• Взрывной урон от {stat} критически важен в PvP.",
        "r_p_ar": "• PvP Attack Rate зависит от AGI → помогает попадать по врагам.",
        "r_p_dr": "• PvP Defense Rate (AGI) помогает уклоняться от ударов.",
        "r_p_sd": "• SD = (все статы)×1.2 + Lvl²/30 → важен баланс статов.",
        "r_p_high": "• {stat} получает больше всего очков ({pct}%) для макс. урона."
    },
    "az": {
        "app_title": "⚔  MuRuZ Character Build Helper  ⚔",
        "app_sub": "Ağıllı stat optimizatoru  ·  Formullara əsaslanan tövsiyələr",
        "char_class": "OYUNÇU SİNİFİ",
        "prog": "İNKİŞAF (PROGRESSION)",
        "rst": "Reset Sayı",
        "lvl": "Cari Səviyyə (Level)",
        "curr_stats": "MÖVCUD STATLAR",
        "rem_pts": "Qalan Xal",
        "vit_opt": "Vitality (VIT) verilsin?\n(Paltardan kifayət qədər HP gəlirsə, söndürün)",
        "calc_btn": "⚡Hesabla",
        "calc_loading": "Hesablanır...",
        "recs": "TÖVSİYƏ EDİLƏN BİLDLƏR",
        "placeholder": ("\n\n   Oyunçu sinifinizi seçib xallarınızı daxil edin,\n"
                        "   daha sonra⚡Hesabla düyməsinə klikləyərək\n"
                        "   optimizasiya olunmuş nəticələri görün.\n"),
        "analysis": "Təhlil və Səbəb",
        
        "err_num": "{name} üçün düzgün rəqəm daxil edin.",
        "err_lvl": "Səviyyə 1 ilə 400 arasında olmalıdır.",
        "err_rst": "Reset sayı mənfi ola bilməz.",
        "err_rem": "Qalan xal mənfi ola bilməz.",
        "err_base": "{stat} xalı {base}-dən az ola bilməz.",
        "err_miss": "Cəmi {form:,} xalınız var, lakin {act:,} qeyd edilib. {diff:,} xal əksikdir.",
        "warn_title": "Xəbərdarlıq",
        "warn_msg": "{err}\n\nYenə də formullar yaradılacaq.",
        
        "info_pts": "Formul üzrə xal: {pts:,}",
        
        "farm_lbl": "🌾 FARM BİLDİ",
        "pve_lbl": "🛡️ PvE BİLDİ",
        "pvp_lbl": "⚔️ PvP BİLDİ",
        "farm_focus": "Sürətli mob kəsimi · Kütləvi zərər · Dayanıqlıq",
        "pve_focus": "Zərər və dözümlülük balansı · Boss döyüşləri",
        "pvp_focus": "Böyük ani zərər (Burst) · Dəqiqlik · Müdafiə",
        
        "exp_total": "Paylanıla bilən ümumi xal: {pts:,}",
        "exp_form": "  Formul: Səv. {lvl} × {ppl} xal/səv. + {rst} res. × 350 xal = {form:,}",
        "exp_bonus": "  + {bonus:,} bonus xal (MMA / kvestlər / eventlər)",
        "exp_alloc": "Xalların paylanması:",
        "exp_pct": "% (xalların hissəsi)",
        "exp_der": "Əsas əlavə göstəricilər:",
        "der_dmg": "Orta Zərər:",
        "der_combo": "Kombo Zərəri:",
        "der_spd": "Hücum Sürəti:",
        "der_def": "Müdafiə (Defense):",
        "der_hp": "HP (VIT-dən):",
        "der_sd": "Qalxan Müdafiəsi (SD):",
        "der_skill": "Bacarıl Qüvvəsi (Skill%):",
        "der_pvm_ar": "PvM Hücum Şansı:",
        "der_pvm_dr": "PvM Müdafiə Şansı:",
        "der_pvp_ar": "PvP Hücum Şansı:",
        "der_pvp_dr": "PvP Müdafiə Şansı:",
        "exp_rsn": "Səbəblər:",
        
        "r_vit_skip": "• VIT-ə xal verilmədi, çünki əşyalardan kifayət qədər HP gəldiyi nəzərə alındı.",
        "r_f_prim": "• Əsas zərər {stat} üzərindən hesablanır.",
        "r_f_spd": "• Hücum sürəti = {form} — daha çox AGI = mobların daha tez ölümü.",
        "r_f_aoe": "• Bacarıq% kütləvi zərəri artırır → daha səmərəli farm.",
        "r_f_vit": "• VIT aşağı saxlanıldı — sağ qalmaq üçün iksirlər bəs edir.",
        "r_f_high": "• Zərər və sürətin ən yaxşı kombinasiyası üçün ən çox xal ({pct}%) {stat}-a verildi.",
        
        "r_e_bal": "• Zərər ({stat}) və sağ qalmaq (VIT/AGI) arasında balans quruldu.",
        "r_e_def": "• Müdafiə = {form} — AGI bosslardan gələn zərəri azaldır.",
        "r_e_vit": "• Daha çox VIT = daha çox HP → ağır boss vuruşlarına dözüm.",
        "r_e_skill": "• Bacarıq% (Skill%) əlavə mobları tez təmizləmək üçün vacibdir.",
        "r_e_high": "• Ən yüksək xal ({pct}%) {stat}-a verildi ki, həm zərər vurulsun həm də çox yatmasın.",
        
        "r_p_brst": "• Oyunçuları tez öldürmək üçün {stat}-dan gələn burst (böyük) zərər mütləqdir.",
        "r_p_ar": "• PvP Attack Rate (Hücum dəqiqliyi) AGI ilə artır → rəqibə vurmaq üçün şərtdir.",
        "r_p_dr": "• PvP Defense Rate (AGI) zərbələrdən yayınmağa kömək edir.",
        "r_p_sd": "• SD = (bütün xallar)×1.2 + Lvl²/30 → balanslı stats PvP-də SD-ni yüksəldir.",
        "r_p_high": "• Maksimum PvP performansı üçün {stat}-a ən çox xal ({pct}%) verildi."
    }
}

def get_text(lang_code, key, **kwargs):
    text = TEXTS.get(lang_code, TEXTS["en"]).get(key, TEXTS["en"].get(key, ""))
    if kwargs:
        return text.format(**kwargs)
    return text
