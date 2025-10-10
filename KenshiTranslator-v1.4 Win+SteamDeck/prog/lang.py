# ⚠️ Остальные языки остаются без изменений (вся структура из исходного файла)
# Украинский, Русский, Deutsch, Français, Español, Português (Brasil), Italiano, Polski, Nederlands,
# Türkçe, Čeština, Magyar, Srpski, Română, Ελληνικά, Български, 日本語, 한국어, 中文（简体）
import os
import json
import tkinter as tk

LANG_FILE = "lang.json"
SETTINGS_FILE = "settings.json"

# ================== БЕЗОПАСНАЯ ЗАГРУЗКА ЯЗЫКА ==================
if os.path.exists(SETTINGS_FILE):
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        lang_name = settings.get("language", "English")
    except Exception:
        lang_name = "English"
else:
    lang_name = "English"

if os.path.exists(LANG_FILE):
    try:
        with open(LANG_FILE, "r", encoding="utf-8") as f:
            lang_data = json.load(f)
    except Exception:
        lang_data = {"English": {"messages": {}, "buttons": {}}}
else:
    lang_data = {"English": {"messages": {}, "buttons": {}}}

LANG = lang_data.get(lang_name, lang_data.get("English", {}))

# ================== ВСТРОЕННЫЙ ШАБЛОН ==================
LANGS = {
  "English": {
    "buttons": {
      "1": "Scan Mods",
      "2": "Load Conf.",
      "3": "Sort Mods",
      "4": "Save Conf.",
      "5": "Clear",
      "6": "My Game",
      "7": "Translate",
      "8": "Start Kenshi",
      "9": "Exit",
      "10": "Action 2",
      "11": "Action 3",
      "12": "Action 4",
      "13": "Action 5",
      "14": "Back"
    },
    "messages": {
      "1": "MOD LIST DELETED",
      "2": "ERROR DELETING FILE",
      "3": "PRESS SCAN MOD",
      "4": "FOLDER FOUND",
      "5": "LOCAL FOUND",
      "6": "KENSHI NOT FOUND",
      "7": "INSTALL TO CORRECT LOCATION",
      "8": "INSTALL",
      "9": "READY",
      "10": "OLD MOD LIST DELETED",
      "11": "SCAN COMPLETE: {count} MODS",
      "12": "SORTING COMPLETE",
      "13": "SORTING ERROR: {error}",
      "14": "{mod_name} ENABLED/DISABLED",
      "15": "RIGHT-CLICK: {mod_name} WRITTEN TO MODS_ALL.JSON",
      "16": "RIGHT-CLICK SAVE ERROR: {error}",
      "17": "PROFILE {idx} SAVED",
      "18": "PROFILE {idx} NOT FOUND",
      "19": "PROFILE {idx} EMPTY",
      "20": "PROFILE {idx} HAS NO MODS",
      "21": "PROFILE {idx} LOADED",
      "22": "NO MODS TO SAVE",
      "23": "MOD CFG LOADED",
      "24": "CFG SAVED / BACKUP CREATED",
      "25": "LOADED FROM MODS.CFG",
      "26": "SAVED {count} MODS, CFG → {backup}",
      "27": "Name",
      "28": "Author",
      "29": "Version",
      "30": "Language",
      "31": "Steam ID",
      "32": "Links",
      "33": "Updated",
      "34": "Dependencies",
      "35": "KENSHI NOT FOUND",
      "36": "ERROR STARTING KENSHI: {error}",
      "37": "ERROR SETTINGS NOT FOUND",
      "38": "MODS NOT FOUND",
      "39": "PRESS SCAN MOD",
      "40": "SORTED {count} ENTRIES"
    }
  },

  "Українська": {
    "buttons": {
      "1": "Скан Моди",
      "2": "Завант. Конф.",
      "3": "Сорт. Моди",
      "4": "Збер. Конф.",
      "5": "Очищення",
      "6": "Моя Гра",
      "7": "Перекл.",
      "8": "Старт Kenshi",
      "9": "Вихід",
      "10": "Дія 2",
      "11": "Дія 3",
      "12": "Дія 4",
      "13": "Дія 5",
      "14": "Назад"
    },
    "messages": {
      "1": "СПИСОК МОДІВ ВИДАЛЕНО",
      "2": "ПОМИЛКА ВИДАЛЕННЯ ФАЙЛУ",
      "3": "НАТИСНІТЬ СКАН МОД",
      "4": "ТЕКУ ЗНАЙДЕНО",
      "5": "ЛОКАЛЬ ЗНАЙДЕНО",
      "6": "KENSHI НЕ ЗНАЙДЕНО",
      "7": "ВСТАНОВІТЬ ДО ПРАВИЛЬНОЇ ТЕКИ",
      "8": "ВСТАНОВЛЕННЯ",
      "9": "ГОТОВО",
      "10": "СТАРИЙ СПИСОК МОДІВ ВИДАЛЕНО",
      "11": "СКАН ЗАВЕРШЕНО: {count} МОДІВ",
      "12": "СОРТУВАННЯ ЗАВЕРШЕНО",
      "13": "ПОМИЛКА СОРТУВАННЯ: {error}",
      "14": "{mod_name} УВІМК./ВИМК.",
      "15": "ПКМ: {mod_name} ЗАПИСАНО В MODS_ALL.JSON",
      "16": "ПОМИЛКА ЗБЕРЕЖЕННЯ ПКМ: {error}",
      "17": "ПРОФІЛЬ {idx} ЗБЕРЕЖЕНО",
      "18": "ПРОФІЛЬ {idx} НЕ ЗНАЙДЕНО",
      "19": "ПРОФІЛЬ {idx} ПУСТИЙ",
      "20": "ПРОФІЛЬ {idx} НЕ МАЄ МОДІВ",
      "21": "ПРОФІЛЬ {idx} ЗАВАНТАЖЕНО",
      "22": "НЕМАЄ МОДІВ ДЛЯ ЗБЕРЕЖЕННЯ",
      "23": "КОНФІГ МОДІВ ЗАВАНТАЖЕНО",
      "24": "ЗБЕРЕЖЕНО / РЕЗЕРВ СТВОРЕНО",
      "25": "ЗАВАНТАЖЕНО З MODS.CFG",
      "26": "ЗБЕРЕЖЕНО {count} МОДІВ, CFG → {backup}",
      "27": "Назва",
      "28": "Автор",
      "29": "Версія",
      "30": "Мова",
      "31": "Steam ID",
      "32": "Посилання",
      "33": "Оновлено",
      "34": "Залежності",
      "35": "KENSHI НЕ ЗНАЙДЕНО",
      "36": "ПОМИЛКА СТАРТУ KENSHI: {error}",
      "37": "НАЛАШТУВАННЯ НЕ ЗНАЙДЕНО",
      "38": "МОДИ НЕ ЗНАЙДЕНО",
      "39": "НАТИСНІТЬ СКАН МОД",
      "40": "ВІДСОРТОВАНО {count} ЗАПИСІВ"
    }
  },

  "Русский": {
    "buttons": {
      "1": "Скан Моды",
      "2": "Загр. Конф.",
      "3": "Сорт. Моды",
      "4": "Сохр. Конф.",
      "5": "Очистка",
      "6": "Моя Игра",
      "7": "Перевод",
      "8": "Старт Kenshi",
      "9": "Выход",
      "10": "Действ. 2",
      "11": "Действ. 3",
      "12": "Действ. 4",
      "13": "Действ. 5",
      "14": "Назад"
    },
    "messages": {
      "1": "СПИСОК МОДОВ УДАЛЕН",
      "2": "ОШИБКА УДАЛЕНИЯ ФАЙЛА",
      "3": "НАЖМИТЕ СКАН МОД",
      "4": "ПАПКА НАЙДЕНА",
      "5": "ЛОКАЛЬ НАЙДЕНА",
      "6": "KENSHI НЕ НАЙДЕН",
      "7": "УСТАНОВИТЕ В ПРАВИЛЬНУЮ ПАПКУ",
      "8": "УСТАНОВКА",
      "9": "ГОТОВО",
      "10": "СТАРЫЙ СПИСОК МОДОВ УДАЛЕН",
      "11": "СКАНИРОВАНИЕ ЗАВЕРШЕНО: {count} МОДОВ",
      "12": "СОРТИРОВКА ЗАВЕРШЕНА",
      "13": "ОШИБКА СОРТИРОВКИ: {error}",
      "14": "{mod_name} ВКЛЮЧЕН/ВЫКЛЮЧЕН",
      "15": "ПКМ: {mod_name} ЗАПИСАН В MODS_ALL.JSON",
      "16": "ОШИБКА СОХРАНЕНИЯ ПКМ: {error}",
      "17": "ПРОФИЛЬ {idx} СОХРАНЕН",
      "18": "ПРОФИЛЬ {idx} НЕ НАЙДЕН",
      "19": "ПРОФИЛЬ {idx} ПУСТОЙ",
      "20": "ПРОФИЛЬ {idx} БЕЗ МОДОВ",
      "21": "ПРОФИЛЬ {idx} ЗАГРУЖЕН",
      "22": "НЕТ МОДОВ ДЛЯ СОХРАНЕНИЯ",
      "23": "КОНФИГ МОДОВ ЗАГРУЖЕН",
      "24": "СОХРАНЕН / СОЗДАН БЭКАП",
      "25": "ЗАГРУЖЕНО ИЗ MODS.CFG",
      "26": "СОХРАНЕНО {count} МОДОВ, CFG → {backup}",
      "27": "Название",
      "28": "Автор",
      "29": "Версия",
      "30": "Язык",
      "31": "Steam ID",
      "32": "Ссылки",
      "33": "Обновлено",
      "34": "Зависимости",
      "35": "KENSHI НЕ НАЙДЕН",
      "36": "ОШИБКА ЗАПУСКА KENSHI: {error}",
      "37": "НАСТРОЙКИ НЕ НАЙДЕНЫ",
      "38": "МОДЫ НЕ НАЙДЕНЫ",
      "39": "НАЖМИТЕ СКАН МОД",
      "40": "ОТСОРТИРОВАНО {count} ЗАПИСЕЙ"
    }
  },

  "Deutsch": {
    "buttons": {
      "1": "Scan Mods",
      "2": "Lad. Konf.",
      "3": "Sort Mods",
      "4": "Speich. Konf.",
      "5": "Leeren",
      "6": "Mein Spiel",
      "7": "Übersetz.",
      "8": "Start Kenshi",
      "9": "Beenden",
      "10": "Aktion 2",
      "11": "Aktion 3",
      "12": "Aktion 4",
      "13": "Aktion 5",
      "14": "Zurück"
    },
    "messages": {
      "1": "MODLISTE GELÖSCHT",
      "2": "FEHLER BEIM LÖSCHEN",
      "3": "SCAN MOD DRÜCKEN",
      "4": "ORDNER GEFUNDEN",
      "5": "LOKAL GEFUNDEN",
      "6": "KENSHI NICHT GEFUNDEN",
      "7": "INSTALLIERE AN RICHTIGEN ORT",
      "8": "INSTALLATION",
      "9": "BEREIT",
      "10": "ALTE MODLISTE GELÖSCHT",
      "11": "SCAN ABGESCHLOSSEN: {count} MODS",
      "12": "SORTIERUNG ABGESCHLOSSEN",
      "13": "SORTIERFEHLER: {error}",
      "14": "{mod_name} AKTIVIERT/DEAKTIVIERT",
      "15": "R-KLICK: {mod_name} IN MODS_ALL.JSON GESCHRIEBEN",
      "16": "R-KLICK SPEICHERFEHLER: {error}",
      "17": "PROFIL {idx} GESPEICHERT",
      "18": "PROFIL {idx} NICHT GEFUNDEN",
      "19": "PROFIL {idx} LEER",
      "20": "PROFIL {idx} HAT KEINE MODS",
      "21": "PROFIL {idx} GELADEN",
      "22": "KEINE MODS ZUM SPEICHERN",
      "23": "MOD KONFIG GELADEN",
      "24": "KONFIG GESPEICHERT / BACKUP ERSTELLT",
      "25": "GELADEN AUS MODS.CFG",
      "26": "{count} MODS GESPEICHERT, CFG → {backup}",
      "27": "Name",
      "28": "Autor",
      "29": "Version",
      "30": "Sprache",
      "31": "Steam ID",
      "32": "Links",
      "33": "Aktualisiert",
      "34": "Abhängigkeiten",
      "35": "KENSHI NICHT GEFUNDEN",
      "36": "FEHLER START KENSHI: {error}",
      "37": "EINSTELLUNGEN NICHT GEFUNDEN",
      "38": "MODS NICHT GEFUNDEN",
      "39": "SCAN MOD DRÜCKEN",
      "40": "{count} EINTRÄGE SORTIERT"
    }
  },

  "Français": {
    "buttons": {
      "1": "Scan Mods",
      "2": "Charg. Conf.",
      "3": "Tri Mods",
      "4": "Enreg. Conf.",
      "5": "Vider",
      "6": "Mon Jeu",
      "7": "Traduire",
      "8": "Démarr. Kenshi",
      "9": "Quitter",
      "10": "Action 2",
      "11": "Action 3",
      "12": "Action 4",
      "13": "Action 5",
      "14": "Retour"
    },
    "messages": {
      "1": "LISTE DE MODS SUPPRIMÉE",
      "2": "ERREUR SUPPRESSION FICHIER",
      "3": "APPUYEZ SUR SCAN MOD",
      "4": "DOSSIER TROUVÉ",
      "5": "LOCAL TROUVÉ",
      "6": "KENSHI INTROUVABLE",
      "7": "INSTALLER DANS BON EMPLACEMENT",
      "8": "INSTALLATION",
      "9": "PRÊT",
      "10": "ANCIENNE LISTE DE MODS SUPPRIMÉE",
      "11": "SCAN TERMINÉ: {count} MODS",
      "12": "TRI TERMINÉ",
      "13": "ERREUR TRI: {error}",
      "14": "{mod_name} ACTIVÉ/DÉSACTIVÉ",
      "15": "CLIC DROIT: {mod_name} ÉCRIT DANS MODS_ALL.JSON",
      "16": "ERREUR SAUVEGARDE CLIC DROIT: {error}",
      "17": "PROFIL {idx} ENREGISTRÉ",
      "18": "PROFIL {idx} INTROUVABLE",
      "19": "PROFIL {idx} VIDE",
      "20": "PROFIL {idx} N’A PAS DE MODS",
      "21": "PROFIL {idx} CHARGÉ",
      "22": "AUCUN MOD À ENREGISTRER",
      "23": "CONFIG MOD CHARGÉE",
      "24": "CONFIG ENREGISTRÉE / SAUVEGARDE CRÉÉE",
      "25": "CHARGÉ DEPUIS MODS.CFG",
      "26": "{count} MODS ENREGISTRÉS, CFG → {backup}",
      "27": "Nom",
      "28": "Auteur",
      "29": "Version",
      "30": "Langue",
      "31": "Steam ID",
      "32": "Liens",
      "33": "Mis à jour",
      "34": "Dépendances",
      "35": "KENSHI INTROUVABLE",
      "36": "ERREUR DÉMARRAGE KENSHI: {error}",
      "37": "PARAMÈTRES INTROUVABLES",
      "38": "MODS INTROUVABLES",
      "39": "APPUYEZ SUR SCAN MOD",
      "40": "{count} ENTRÉES TRIÉES"
    }
  },
  
  "Español": {
    "buttons": {
      "1": "Escan. Mods",
      "2": "Carg. Conf.",
      "3": "Orden. Mods",
      "4": "Guard. Conf.",
      "5": "Borrar",
      "6": "Mi Juego",
      "7": "Traducir",
      "8": "Inic. Kenshi",
      "9": "Salir",
      "10": "Acción 2",
      "11": "Acción 3",
      "12": "Acción 4",
      "13": "Acción 5",
      "14": "Atrás"
    },
    "messages": {
      "1": "LISTA DE MODS ELIMINADA",
      "2": "ERROR AL ELIMINAR ARCHIVO",
      "3": "PRESIONE ESCAN. MOD",
      "4": "CARPETA ENCONTRADA",
      "5": "LOCAL ENCONTRADO",
      "6": "KENSHI NO ENCONTRADO",
      "7": "INSTALE EN UBICACIÓN CORRECTA",
      "8": "INSTALACIÓN",
      "9": "LISTO",
      "10": "LISTA DE MODS ANTIGUA ELIMINADA",
      "11": "ESCANEO COMPLETO: {count} MODS",
      "12": "ORDEN COMPLETA",
      "13": "ERROR ORDENANDO: {error}",
      "14": "{mod_name} ACTIVADO/DESACTIVADO",
      "15": "CLIC DER: {mod_name} ESCRITO EN MODS_ALL.JSON",
      "16": "ERROR GUARDAR CLIC DER: {error}",
      "17": "PERFIL {idx} GUARDADO",
      "18": "PERFIL {idx} NO ENCONTRADO",
      "19": "PERFIL {idx} VACÍO",
      "20": "PERFIL {idx} NO TIENE MODS",
      "21": "PERFIL {idx} CARGADO",
      "22": "NO HAY MODS PARA GUARDAR",
      "23": "CONFIG MOD CARGADA",
      "24": "CONFIG GUARDADA / BACKUP CREADO",
      "25": "CARGADO DESDE MODS.CFG",
      "26": "GUARDADOS {count} MODS, CFG → {backup}",
      "27": "Nombre",
      "28": "Autor",
      "29": "Versión",
      "30": "Idioma",
      "31": "Steam ID",
      "32": "Enlaces",
      "33": "Actualizado",
      "34": "Dependencias",
      "35": "KENSHI NO ENCONTRADO",
      "36": "ERROR INICIANDO KENSHI: {error}",
      "37": "CONFIGURACIÓN NO ENCONTRADA",
      "38": "MODS NO ENCONTRADOS",
      "39": "PRESIONE ESCAN. MOD",
      "40": "ORDENADOS {count} ELEMENTOS"
    }
  },

  "Português (Brasil)": {
    "buttons": {
      "1": "Scan Mods",
      "2": "Carreg. Conf.",
      "3": "Ord. Mods",
      "4": "Salvar Conf.",
      "5": "Limpar",
      "6": "Meu Jogo",
      "7": "Traduzir",
      "8": "Inic. Kenshi",
      "9": "Sair",
      "10": "Ação 2",
      "11": "Ação 3",
      "12": "Ação 4",
      "13": "Ação 5",
      "14": "Voltar"
    },
    "messages": {
      "1": "LISTA DE MODS EXCLUÍDA",
      "2": "ERRO AO EXCLUIR ARQUIВО",
      "3": "PRESSIONE SCAN MOD",
      "4": "PASTA ENCONTRADA",
      "5": "LOCAL ENCONTRADO",
      "6": "KENSHI NÃO ENCONTRADO",
      "7": "INSTALE NO LOCAL CORRETO",
      "8": "INSTALAÇÃO",
      "9": "PRONTO",
      "10": "LISTA ANTIGA DE MODS EXCLUÍDA",
      "11": "SCAN COMPLETO: {count} MODS",
      "12": "ORDENAÇÃO CONCLUÍДА",
      "13": "ERRO NA ORDENAÇÃO: {error}",
      "14": "{mod_name} ATIVADO/DESATIVADO",
      "15": "CLIQUE DIR: {mod_name} GRAVADO EM MODS_ALL.JSON",
      "16": "ERRO AO SALVAR CLIQUE DIR: {error}",
      "17": "PERFIL {idx} SALVO",
      "18": "PERFIL {idx} NÃO ENCONTRADO",
      "19": "PERFIL {idx} VAZIO",
      "20": "PERFIL {idx} SEM MODS",
      "21": "PERFIL {idx} CARREGADO",
      "22": "NENHUM MOD PARA SALVAR",
      "23": "CFG MOD CARREGADO",
      "24": "CFG SALVO / BACKUP CRIADO",
      "25": "CARREGADO DE MODS.CFG",
      "26": "SALVOS {count} MODS, CFG → {backup}",
      "27": "Nome",
      "28": "Autor",
      "29": "Versão",
      "30": "Idioma",
      "31": "Steam ID",
      "32": "Links",
      "33": "Atualizado",
      "34": "Dependências",
      "35": "KENSHI NÃO ENCONTRADO",
      "36": "ERRO AO INICIAR KENSHI: {error}",
      "37": "CONFIGURAÇÕES NÃO ENCONTRADAS",
      "38": "MODS NÃO ENCONTRADOS",
      "39": "PRESSIONE SCAN MOD",
      "40": "ORDENADOS {count} ITENS"
    }
  },

  "Italiano": {
    "buttons": {
      "1": "Scans. Mods",
      "2": "Caric. Conf.",
      "3": "Ord. Mods",
      "4": "Salv. Conf.",
      "5": "Pulisci",
      "6": "Mio Gioco",
      "7": "Traduci",
      "8": "Avvia Kenshi",
      "9": "Uscita",
      "10": "Azione 2",
      "11": "Azione 3",
      "12": "Azione 4",
      "13": "Azione 5",
      "14": "Indietro"
    },
    "messages": {
      "1": "LISTA MOD ELIMINATA",
      "2": "ERRORE ELIMINAZIONE FILE",
      "3": "PREMI SCANS. MOD",
      "4": "CARTELLA TROVATA",
      "5": "LOCALE TROVATO",
      "6": "KENSHI NON TROVATO",
      "7": "INSTALLA NELLA CARTELLA CORRETTA",
      "8": "INSTALLAZIONE",
      "9": "PRONTO",
      "10": "VECCHIA LISTA MOD ELIMINATA",
      "11": "SCANSIONE COMPLETA: {count} MODS",
      "12": "ORDINAMENTO COMPLETATO",
      "13": "ERRORE ORDINAMENTO: {error}",
      "14": "{mod_name} ABILITATO/DISABILITATO",
      "15": "CLIC DESTRO: {mod_name} SCRITTO IN MODS_ALL.JSON",
      "16": "ERRORE SALVATAGGIO CL. DESTRO: {error}",
      "17": "PROFILO {idx} SALVATO",
      "18": "PROFILO {idx} NON TROVATO",
      "19": "PROFILO {idx} VUOTO",
      "20": "PROFILO {idx} SENZA MODS",
      "21": "PROFILO {idx} CARICATO",
      "22": "NESSUN MOD DA SALVARE",
      "23": "CFG MOD CARICATO",
      "24": "CFG SALVATO / BACKUP CREATO",
      "25": "CARICATO DA MODS.CFG",
      "26": "SALVATI {count} MODS, CFG → {backup}",
      "27": "Nome",
      "28": "Autore",
      "29": "Versione",
      "30": "Lingua",
      "31": "Steam ID",
      "32": "Link",
      "33": "Aggiornato",
      "34": "Dipendenze",
      "35": "KENSHI NON TROVATO",
      "36": "ERRORE AVVIO KENSHI: {error}",
      "37": "IMPOSTAZIONI NON TROVATE",
      "38": "MODS NON TROVATI",
      "39": "PREMI SCANS. MOD",
      "40": "{count} VOCI ORDINATE"
    }
  },

  "Polski": {
    "buttons": {
      "1": "Skan. Mody",
      "2": "Wczyt. Konf.",
      "3": "Sort. Mody",
      "4": "Zapisz Konf.",
      "5": "Wyczyść",
      "6": "Moja Gra",
      "7": "Tłumacz",
      "8": "Start Kenshi",
      "9": "Wyjście",
      "10": "Akcja 2",
      "11": "Akcja 3",
      "12": "Akcja 4",
      "13": "Akcja 5",
      "14": "Wstecz"
    },
    "messages": {
      "1": "LISTA MODÓW USUNIĘTA",
      "2": "BŁĄD USUWANIA PLIKU",
      "3": "NACIŚNIJ SKAN. MOD",
      "4": "FOLDER ZNALEZIONY",
      "5": "LOKAL ZNALEZIONY",
      "6": "KENSHI NIE ZNALEZIONO",
      "7": "ZAINSTALUJ WE WŁAŚCIWEJ LOKALIZACJI",
      "8": "INSTALACJA",
      "9": "GOTOWE",
      "10": "STARA LISTA MODÓW USUNIĘTA",
      "11": "SKAN ZAKOŃCZONY: {count} MODÓW",
      "12": "SORTOWANIE ZAKOŃCZONE",
      "13": "BŁĄD SORTOWANIA: {error}",
      "14": "{mod_name} WŁĄCZONY/WYŁĄCZONY",
      "15": "PRAWY KLIK: {mod_name} ZAPISANY DO MODS_ALL.JSON",
      "16": "BŁĄD ZAPISU PRAWYM KLIKIEM: {error}",
      "17": "PROFIL {idx} ZAPISANY",
      "18": "PROFIL {idx} NIE ZNALEZIONY",
      "19": "PROFIL {idx} PUSTY",
      "20": "PROFIL {idx} NIE MA MODÓW",
      "21": "PROFIL {idx} WCZYTANY",
      "22": "BRAK MODÓW DO ZAPISU",
      "23": "KONFIG MODÓW WCZYTANY",
      "24": "KONFIG ZAPISANY / BACKUP UTWORZONY",
      "25": "WCZYTANO Z MODS.CFG",
      "26": "ZAPISANO {count} MODÓW, CFG → {backup}",
      "27": "Nazwa",
      "28": "Autor",
      "29": "Wersja",
      "30": "Język",
      "31": "Steam ID",
      "32": "Linki",
      "33": "Zaktualizowano",
      "34": "Zależności",
      "35": "KENSHI NIE ZNALEZIONO",
      "36": "BŁĄD URUCHAMIANIA KENSHI: {error}",
      "37": "USTAWIENIA NIE ZNALEZIONE",
      "38": "MODY NIE ZNALEZIONE",
      "39": "NACIŚNIJ SKAN. MOD",
      "40": "POSORTOWANO {count} WPISÓW"
    }
  },

  "Nederlands": {
    "buttons": {
      "1": "Scan Mods",
      "2": "Laad Conf.",
      "3": "Sorteer Mods",
      "4": "Bewaar Conf.",
      "5": "Wissen",
      "6": "Mijn Spel",
      "7": "Vertalen",
      "8": "Start Kenshi",
      "9": "Afsluit.",
      "10": "Actie 2",
      "11": "Actie 3",
      "12": "Actie 4",
      "13": "Actie 5",
      "14": "Terug"
    },
    "messages": {
      "1": "MODLIJST VERWIJDERD",
      "2": "FOUT BIJ VERWIJDEREN BESTAND",
      "3": "DRUK OP SCAN MOD",
      "4": "MAP GEVONDEN",
      "5": "LOKAAL GEVONDEN",
      "6": "KENSHI NIET GEVONDEN",
      "7": "INSTALLEER OP JUISTE LOCATIE",
      "8": "INSTALLATIE",
      "9": "KLAAR",
      "10": "OUDE MODLIJST VERWIJDERD",
      "11": "SCAN VOLTOOID: {count} MODS",
      "12": "SORTEREN VOLTOOID",
      "13": "SORTERINGSFOUT: {error}",
      "14": "{mod_name} INGESCHAKELD/UITGESCHAKELD",
      "15": "RECHTERKLIK: {mod_name} GESCHREVEN NAAR MODS_ALL.JSON",
      "16": "FOUT OPSLAAN RECHTERKLIK: {error}",
      "17": "PROFIEL {idx} OPGESLAGEN",
      "18": "PROFIEL {idx} NIET GEVONDEN",
      "19": "PROFIEL {idx} LEEG",
      "20": "PROFIEL {idx} HEEFT GEEN MODS",
      "21": "PROFIEL {idx} GELADEN",
      "22": "GEEN MODS OM OP TE SLAAN",
      "23": "MOD CONFIG GELADEN",
      "24": "CONFIG OPGESLAGEN / BACKUP GEMAAKT",
      "25": "GELADEN VAN MODS.CFG",
      "26": "{count} MODS OPGESLAGEN, CFG → {backup}",
      "27": "Naam",
      "28": "Auteur",
      "29": "Versie",
      "30": "Taal",
      "31": "Steam ID",
      "32": "Links",
      "33": "Bijgewerkt",
      "34": "Afhankelijkheden",
      "35": "KENSHI NIET GEVONDEN",
      "36": "FOUT STARTEN KENSHI: {error}",
      "37": "INSTELLINGEN NIET GEVONDEN",
      "38": "MODS NIET GEVONDEN",
      "39": "DRUK OP SCAN MOD",
      "40": "{count} ITEMS GESORTEERD"
    }
  },

  "Türkçe": {
    "buttons": {
      "1": "Tara Mods",
      "2": "Yükle Konf.",
      "3": "Sırala Mods",
      "4": "Kaydet Konf.",
      "5": "Temizle",
      "6": "Oyunum",
      "7": "Çevir",
      "8": "Başlat Kenshi",
      "9": "Çıkış",
      "10": "Eylem 2",
      "11": "Eylem 3",
      "12": "Eylem 4",
      "13": "Eylem 5",
      "14": "Geri"
    },
    "messages": {
      "1": "MOD LİSTESİ SİLİNDİ",
      "2": "DOSYA SİLME HATASI",
      "3": "SCAN MOD'A BASIN",
      "4": "KLASÖR BULUNDU",
      "5": "LOKAL BULUNDU",
      "6": "KENSHI BULUNAMADI",
      "7": "DOĞRU KONUMA KURUN",
      "8": "KURULUM",
      "9": "HAZIR",
      "10": "ESKİ MOD LİSTESİ SİLİNDİ",
      "11": "TARAMA TAMAMLANDI: {count} MOD",
      "12": "SIRALAMA TAMAMLANDI",
      "13": "SIRALAMA HATASI: {error}",
      "14": "{mod_name} AÇIK/KAPALI",
      "15": "SAĞ TIK: {mod_name} MODS_ALL.JSON'A YAZILDI",
      "16": "SAĞ TIK KAYIT HATASI: {error}",
      "17": "PROFİL {idx} KAYDEDİLDİ",
      "18": "PROFİL {idx} BULUNAMADI",
      "19": "PROFİL {idx} BOŞ",
      "20": "PROFİL {idx} MOD İÇERMİYOR",
      "21": "PROFİL {idx} YÜKLENDİ",
      "22": "KAYDEDİLECEK MOD YOK",
      "23": "MOD KONF. YÜKLENDİ",
      "24": "KONF. KAYDEDİLDİ / YEDEK OLUŞTURULDU",
      "25": "MODS.CFG'DEN YÜKLENDİ",
      "26": "{count} MOD KAYDEDİLDİ, CFG → {backup}",
      "27": "Ad",
      "28": "Yazar",
      "29": "Sürüm",
      "30": "Dil",
      "31": "Steam ID",
      "32": "Bağlantılar",
      "33": "Güncellendi",
      "34": "Bağımlılıklar",
      "35": "KENSHI BULUNAMADI",
      "36": "KENSHI BAŞLATMA HATASI: {error}",
      "37": "AYARLAR BULUNAMADI",
      "38": "MODLAR BULUNAMADI",
      "39": "SCAN MOD'A BASIN",
      "40": "{count} GİRDİ SIRALANDI"
    }
  },

  "Čeština": {
    "buttons": {
      "1": "Sken. Mody",
      "2": "Načíst Konf.",
      "3": "Řadit Mody",
      "4": "Ulož. Konf.",
      "5": "Vymazat",
      "6": "Moje Hra",
      "7": "Přeložit",
      "8": "Spustit Kenshi",
      "9": "Konec",
      "10": "Akce 2",
      "11": "Akce 3",
      "12": "Akce 4",
      "13": "Akce 5",
      "14": "Zpět"
    },
    "messages": {
      "1": "SEZNAM MODŮ SMAZÁN",
      "2": "CHYBA MAZÁNÍ SOUBORU",
      "3": "STISKNĚTE SKEN. MOD",
      "4": "SLOŽKA NALEZENA",
      "5": "LOKÁL NALEZEN",
      "6": "KENSHI NENALEZEN",
      "7": "NAINSTALUJTE DO SPRÁVNÉ SLOŽKY",
      "8": "INSTALACE",
      "9": "PŘIPRAVENO",
      "10": "STARÝ SEZNAM MODŮ SMAZÁN",
      "11": "SKEN DOKONČEN: {count} MODŮ",
      "12": "ŘAZENÍ DOKONČENO",
      "13": "CHYBA ŘAZENÍ: {error}",
      "14": "{mod_name} ZAPNUT/VYPNUT",
      "15": "PKM: {mod_name} ZAPSÁN DO MODS_ALL.JSON",
      "16": "CHYBA UKLÁDÁNÍ PKM: {error}",
      "17": "PROFIL {idx} ULOŽEN",
      "18": "PROFIL {idx} NENALEZEN",
      "19": "PROFIL {idx} PRÁZDNÝ",
      "20": "PROFIL {idx} NEMÁ MODY",
      "21": "PROFIL {idx} NAČTEN",
      "22": "ŽÁDNÉ MODY K ULOŽENÍ",
      "23": "KONFIG MODŮ NAČTEN",
      "24": "KONFIG ULOŽEN / VYTVOŘENA ZÁLOHA",
      "25": "NAČTENO Z MODS.CFG",
      "26": "ULOŽENO {count} MODŮ, CFG → {backup}",
      "27": "Název",
      "28": "Autor",
      "29": "Verze",
      "30": "Jazyk",
      "31": "Steam ID",
      "32": "Odkazy",
      "33": "Aktualizováno",
      "34": "Závislosti",
      "35": "KENSHI NENALEZEN",
      "36": "CHYBA SPUŠTĚNÍ KENSHI: {error}",
      "37": "NASTAVENÍ NENALEZENO",
      "38": "MODY NENALEZENY",
      "39": "STISKNĚTE SKEN. MOD",
      "40": "SEŘAZENO {count} ZÁZNAMŮ"
    }
  },

  "Magyar": {
    "buttons": {
      "1": "Scan Modok",
      "2": "Betölt. Konf.",
      "3": "Rend. Modok",
      "4": "Mentés Konf.",
      "5": "Törlés",
      "6": "Játékom",
      "7": "Fordít",
      "8": "Indít Kenshi",
      "9": "Kilépés",
      "10": "Akció 2",
      "11": "Akció 3",
      "12": "Akció 4",
      "13": "Akció 5",
      "14": "Vissza"
    },
    "messages": {
      "1": "MODLISTA TÖRÖLVE",
      "2": "HIBA A FÁJL TÖRLÉSEKOR",
      "3": "NYOMJON SCAN MOD",
      "4": "MAPPÁT TALÁLT",
      "5": "LOKÁLIS TALÁLT",
      "6": "KENSHI NEM TALÁLHATÓ",
      "7": "TEGYE HELYES HELYRE",
      "8": "TELEPÍTÉS",
      "9": "KÉSZ",
      "10": "RÉGI MODLISTA TÖRÖLVE",
      "11": "SZKENNELÉS KÉSZ: {count} MOD",
      "12": "RENDEZÉS KÉSZ",
      "13": "RENDEZÉSI HIBA: {error}",
      "14": "{mod_name} BEKAPCS./KIKAPCS.",
      "15": "JOBB KATT: {mod_name} ÍRVA MODS_ALL.JSON-BE",
      "16": "JOBB KATT MENTÉSI HIBA: {error}",
      "17": "PROFIL {idx} MENTVE",
      "18": "PROFIL {idx} NEM TALÁLT",
      "19": "PROFIL {idx} ÜRES",
      "20": "PROFIL {idx} NEM TARTALMAZ MODOKAT",
      "21": "PROFIL {idx} BETÖLTVE",
      "22": "NINCS MOD MENTÉSRE",
      "23": "MOD KONFIG BETÖLTVE",
      "24": "KONFIG MENTVE / BIZTONSÁGI MÁSOLAT",
      "25": "BETÖLTVE MODS.CFG-BŐL",
      "26": "{count} MOD MENTVE, CFG → {backup}",
      "27": "Név",
      "28": "Szerző",
      "29": "Verzió",
      "30": "Nyelv",
      "31": "Steam ID",
      "32": "Linkek",
      "33": "Frissítve",
      "34": "Függőségek",
      "35": "KENSHI NEM TALÁLT",
      "36": "HIBA KENSHI INDÍTÁSKOR: {error}",
      "37": "BEÁLLÍTÁSOK NEM TALÁLTAK",
      "38": "MODOK NEM TALÁЛTAK",
      "39": "NYOMJON SCAN MOD",
      "40": "{count} BEJEGYZÉS RENDEZVE"
    }
  },

  "Srpski": {
    "buttons": {
      "1": "Skenir. Mod",
      "2": "Učitaj Konf.",
      "3": "Sortir. Mod",
      "4": "Sačuv. Konf.",
      "5": "Obriši",
      "6": "Moja Igra",
      "7": "Prevodi",
      "8": "Pokreni Kenshi",
      "9": "Izlaz",
      "10": "Akcija 2",
      "11": "Akcija 3",
      "12": "Akcija 4",
      "13": "Akcija 5",
      "14": "Nazad"
    },
    "messages": {
      "1": "LISTA MODOVA OBRISANA",
      "2": "GREŠKA BRISANJA FAJLA",
      "3": "PRITISNI SKENIR. MOD",
      "4": "FOLDER PRONAĐEN",
      "5": "LOKAL PRONAĐEN",
      "6": "KENSHI NIJE PRONAĐEN",
      "7": "INSTALIRAJTE NA PRAVU LOKACIJU",
      "8": "INSTALACIJA",
      "9": "SPREMNO",
      "10": "STARA LISTA MODOVA OBRISANA",
      "11": "SKENIRANJE ZAVRŠENO: {count} MODOVA",
      "12": "SORTIRANJE ZAVRŠENO",
      "13": "GREŠKA SORTIRANJA: {error}",
      "14": "{mod_name} UKLJ./ISKLJ.",
      "15": "DESNI KLIK: {mod_name} UPISAN U MODS_ALL.JSON",
      "16": "GREŠKA ČUVANJA DESNIM KLIKOM: {error}",
      "17": "PROFIL {idx} SAČUVAN",
      "18": "PROFIL {idx} NIJE PRONAĐEN",
      "19": "PROFIL {idx} PRAZAN",
      "20": "PROFIL {idx} NEMA MODOVE",
      "21": "PROFIL {idx} UČITAN",
      "22": "NEMA MODOVA ZA ČUVANJE",
      "23": "MOD KONF. UČITAN",
      "24": "KONF. SAČUVAN / BACKUP NAPRAVLJEN",
      "25": "UČITANO IZ MODS.CFG",
      "26": "SAČUVANO {count} MODOVA, CFG → {backup}",
      "27": "Naziv",
      "28": "Autor",
      "29": "Verzija",
      "30": "Jezik",
      "31": "Steam ID",
      "32": "Linkovi",
      "33": "Ažurirano",
      "34": "Zavisnosti",
      "35": "KENSHI NIJE PRONAĐEN",
      "36": "GREŠKA POKRETANJA KENSHI: {error}",
      "37": "POSTAVKE NISU PRONAĐENE",
      "38": "MODOVI NISU PRONAĐENI",
      "39": "PRITISNI SKENIR. MOD",
      "40": "SORTIRANO {count} UNOSA"
    }
  },

  "Română": {
    "buttons": {
      "1": "Scanare Moduri",
      "2": "Încărc. Conf.",
      "3": "Sortare Moduri",
      "4": "Salv. Conf.",
      "5": "Curățare",
      "6": "Jocul Meu",
      "7": "Traducere",
      "8": "Pornește Kenshi",
      "9": "Ieșire",
      "10": "Acțiune 2",
      "11": "Acțiune 3",
      "12": "Acțiune 4",
      "13": "Acțiune 5",
      "14": "Înapoi"
    },
    "messages": {
      "1": "LISTA DE MODURI ȘTEARSĂ",
      "2": "EROARE LA ȘTERGEREA FIȘIERULUI",
      "3": "APASĂ SCANARE MOD",
      "4": "DOSAR GĂSIT",
      "5": "LOCAL GĂSIT",
      "6": "KENSHI NU A FOST GĂSIT",
      "7": "INSTALEAZĂ ÎN LOCAȚIA CORESPUNZĂTOARE",
      "8": "INSTALARE",
      "9": "GATA",
      "10": "LISTA VECHE DE MODURI ȘTEARSĂ",
      "11": "SCANARE FINALIZATĂ: {count} MODURI",
      "12": "SORTARE FINALIZATĂ",
      "13": "EROARE LA SORTARE: {error}",
      "14": "{mod_name} ACTIVAT/DEZACTIVAT",
      "15": "CLICK DREAPTA: {mod_name} SCRIS ÎN MODS_ALL.JSON",
      "16": "EROARE LA SALVAREA CLICK DREAPTA: {error}",
      "17": "PROFILUL {idx} SALVAT",
      "18": "PROFILUL {idx} NU A FOST GĂSIT",
      "19": "PROFILUL {idx} ESTE GOL",
      "20": "PROFILUL {idx} NU ARE MODURI",
      "21": "PROFILUL {idx} ÎNCĂRCAT",
      "22": "NU EXISTĂ MODURI DE SALVAT",
      "23": "CONFIGURAREA MODURILOR ÎNCĂRCATĂ",
      "24": "CONFIGURAREA SALVATĂ / BACKUP CREAT",
      "25": "ÎNCĂRCAT DIN MODS.CFG",
      "26": "{count} MODURI SALVATE, CFG → {backup}",
      "27": "Nume",
      "28": "Autor",
      "29": "Versiune",
      "30": "Limbă",
      "31": "Steam ID",
      "32": "Linkuri",
      "33": "Actualizat",
      "34": "Dependențe",
      "35": "KENSHI NU A FOST GĂSIT",
      "36": "EROARE LA PORNIREA KENSHI: {error}",
      "37": "SETĂRI NEIDENTIFICATE",
      "38": "MODURI NEIDENTIFICATE",
      "39": "APASĂ SCANARE MOD",
      "40": "S-AU SORTAT {count} ÎNREGISTRĂRI"
    }
  },

  "Ελληνικά": {
    "buttons": {
      "1": "Σάρωση Mods",
      "2": "Φόρτωση Ρυθμ.",
      "3": "Ταξινόμηση Mods",
      "4": "Αποθήκευση Ρυθμ.",
      "5": "Εκκαθάριση",
      "6": "Το Παιχνίδι Μου",
      "7": "Μετάφραση",
      "8": "Έναρξη Kenshi",
      "9": "Έξοδος",
      "10": "Ενέργεια 2",
      "11": "Ενέργεια 3",
      "12": "Ενέργεια 4",
      "13": "Ενέργεια 5",
      "14": "Πίσω"
    },
    "messages": {
      "1": "Η ΛΙΣΤΑ MOD ΔΙΑΓΡΑΦΗΚΕ",
      "2": "ΣΦΑΛΜΑ ΔΙΑΓΡΑΦΗΣ ΑΡΧΕΙΟΥ",
      "3": "ΠΑΤΗΣΤΕ ΣΑΡΩΣΗ MOD",
      "4": "ΒΡΕΘΗΚΕ ΦΑΚΕΛΟΣ",
      "5": "ΒΡΕΘΗΚΕ ΤΟΠΙΚΟ",
      "6": "ΔΕΝ ΒΡΕΘΗΚΕ ΤΟ KENSHI",
      "7": "ΕΓΚΑΤΑΣΤΗΣΤΕ ΣΤΗ ΣΩΣΤΗ ΘΕΣΗ",
      "8": "ΕΓΚΑΤΑΣΤΑΣΗ",
      "9": "ΕΤΟΙΜΟ",
      "10": "ΠΑΛΙΑ ΛΙΣΤΑ MOD ΔΙΑΓΡΑΦΗΚΕ",
      "11": "Η ΣΑΡΩΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ: {count} MODS",
      "12": "Η ΤΑΞΙΝΟΜΗΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ",
      "13": "ΣΦΑΛΜΑ ΤΑΞΙΝΟΜΗΣΗΣ: {error}",
      "14": "{mod_name} ΕΝΕΡΓΟΠΟΙΗΘΗΚΕ/ΑΠΕΝΕΡΓΟΠΟΙΗΘΗΚΕ",
      "15": "ΔΕΞΙ ΚΛΙΚ: {mod_name} ΕΓΓΡΑΦΗΚΕ ΣΤΟ MODS_ALL.JSON",
      "16": "ΣΦΑΛΜΑ ΑΠΟΘΗΚΕΥΣΗΣ ΔΕΞΙΟΥ ΚΛΙΚ: {error}",
      "17": "ΤΟ ΠΡΟΦΙΛ {idx} ΑΠΟΘΗΚΕΥΤΗΚΕ",
      "18": "ΤΟ ΠΡΟΦΙΛ {idx} ΔΕΝ ΒΡΕΘΗΚΕ",
      "19": "ΤΟ ΠΡΟΦΙΛ {idx} ΕΙΝΑΙ ΚΕΝΟ",
      "20": "ΤΟ ΠΡΟΦΙΛ {idx} ΔΕΝ ΕΧΕΙ MODS",
      "21": "ΤΟ ΠΡΟΦΙΛ {idx} ΦΟΡΤΩΘΗΚΕ",
      "22": "ΔΕΝ ΥΠΑΡΧΟΥΝ MODS ΓΙΑ ΑΠΟΘΗΚΕΥΣΗ",
      "23": "ΦΟΡΤΩΘΗΚΕ Η ΔΙΑΜΟΡΦΩΣΗ MOD",
      "24": "Η ΔΙΑΜΟΡΦΩΣΗ ΑΠΟΘΗΚΕΥΤΗΚΕ / ΔΗΜΙΟΥΡΓΗΘΗΚΕ ΑΝΤΙΓΡΑΦΟ ΑΣΦΑΛΕΙΑΣ",
      "25": "ΦΟΡΤΩΘΗΚΕ ΑΠΟ MODS.CFG",
      "26": "ΑΠΟΘΗΚΕΥΤΗΚΑΝ {count} MODS, CFG → {backup}",
      "27": "Όνομα",
      "28": "Συγγραφέας",
      "29": "Έκδοση",
      "30": "Γλώσσα",
      "31": "Steam ID",
      "32": "Σύνδεσμοι",
      "33": "Ενημερώθηκε",
      "34": "Εξαρτήσεις",
      "35": "ΔΕΝ ΒΡΕΘΗΚΕ ΤΟ KENSHI",
      "36": "ΣΦΑΛΜΑ ΕΝΑΡΞΗΣ KENSHI: {error}",
      "37": "ΔΕΝ ΒΡΕΘΗΚΑΝ ΡΥΘΜΙΣΕΙΣ",
      "38": "ΔΕΝ ΒΡΕΘΗΚΑΝ MODS",
      "39": "ΠΑΤΗΣΤΕ ΣΑΡΩΣΗ MOD",
      "40": "ΤΑΞΙΝΟΜΗΘΗΚΑΝ {count} ΕΓΓΡΑΦΕΣ"
    }
  },

  "Български": {
    "buttons": {
      "1": "Сканирай Mod",
      "2": "Зареди Конф.",
      "3": "Сортирай Mod",
      "4": "Запази Конф.",
      "5": "Изчисти",
      "6": "Моята Игра",
      "7": "Преведи",
      "8": "Старт Kenshi",
      "9": "Изход",
      "10": "Дейст. 2",
      "11": "Дейст. 3",
      "12": "Дейст. 4",
      "13": "Дейст. 5",
      "14": "Назад"
    },
    "messages": {
      "1": "СПИСЪК MOD ИЗТРИТ",
      "2": "ГРЕШКА ПРИ ИЗТРИВАНЕ НА ФАЙЛ",
      "3": "НАТИСНИ СКАНИРАЙ MOD",
      "4": "ПАПКА НАМЕРЕНА",
      "5": "ЛОКАЛ НАМЕРЕН",
      "6": "KENSHI НЕ Е НАМЕРЕН",
      "7": "ИНСТАЛИРАЙТЕ НА ПРАВИЛНОТО МЯСТО",
      "8": "ИНСТАЛАЦИЯ",
      "9": "ГОТОВО",
      "10": "СТАР СПИСЪК MOD ИЗТРИТ",
      "11": "СКАНИРАНЕ ЗАВЪРШЕНО: {count} MOD",
      "12": "СОРТИРАНЕ ЗАВЪРШЕНО",
      "13": "ГРЕШКА ПРИ СОРТИРАНЕ: {error}",
      "14": "{mod_name} ВКЛ./ИЗКЛ.",
      "15": "ДЕСЕН КЛИК: {mod_name} ЗАПИСАН В MODS_ALL.JSON",
      "16": "ГРЕШКА ЗАПИС ПРИ ДЕСЕН КЛИК: {error}",
      "17": "ПРОФИЛ {idx} ЗАПАЗЕН",
      "18": "ПРОФИЛ {idx} НЕ Е НАМЕРЕН",
      "19": "ПРОФИЛ {idx} ПРАЗЕН",
      "20": "ПРОФИЛ {idx} НЯМА MOD",
      "21": "ПРОФИЛ {idx} ЗАРЕДЕН",
      "22": "НЯМА MOD ЗА ЗАПАЗВАНЕ",
      "23": "MOD CFG ЗАРЕДЕН",
      "24": "CFG ЗАПАЗЕН / BACKUP СЪЗДАДЕН",
      "25": "ЗАРЕДЕН ОТ MODS.CFG",
      "26": "ЗАПАЗЕНИ {count} MOD, CFG → {backup}",
      "27": "Име",
      "28": "Автор",
      "29": "Версия",
      "30": "Език",
      "31": "Steam ID",
      "32": "Връзки",
      "33": "Обновено",
      "34": "Зависимости",
      "35": "KENSHI НЕ Е НАМЕРЕН",
      "36": "ГРЕШКА СТАРТИРАНЕ НА KENSHI: {error}",
      "37": "НАСТРОЙКИ НЕ НАМЕРЕНИ",
      "38": "MOD НЕ НАМЕРЕНИ",
      "39": "НАТИСНИ СКАНИРАЙ MOD",
      "40": "СОРТИРАНИ {count} ЗАПИСА"
    }
  },

  "日本語": {
    "buttons": {
      "1": "スキャンMod",
      "2": "読込 設定",
      "3": "並べ替え",
      "4": "保存 設定",
      "5": "クリア",
      "6": "マイゲーム",
      "7": "翻訳",
      "8": "開始 Kenshi",
      "9": "終了",
      "10": "操作 2",
      "11": "操作 3",
      "12": "操作 4",
      "13": "操作 5",
      "14": "戻る"
    },
    "messages": {
      "1": "MODリスト削除",
      "2": "ファイル削除エラー",
      "3": "スキャンMOD押下",
      "4": "フォルダ発見",
      "5": "ローカル発見",
      "6": "KENSHI未検出",
      "7": "正しい場所にインストール",
      "8": "インストール",
      "9": "準備完了",
      "10": "古いMODリスト削除",
      "11": "スキャン完了: {count} MOD",
      "12": "並べ替え完了",
      "13": "並べ替えエラー: {error}",
      "14": "{mod_name} 有効/無効",
      "15": "右クリック: {mod_name} MODS_ALL.JSONに書込",
      "16": "右クリック保存エラー: {error}",
      "17": "プロファイル{idx}保存",
      "18": "プロファイル{idx}未検出",
      "19": "プロファイル{idx}空",
      "20": "プロファイル{idx}MODなし",
      "21": "プロファイル{idx}読込",
      "22": "保存するMODなし",
      "23": "MOD設定読込",
      "24": "設定保存 / バックアップ作成",
      "25": "MODS.CFGから読込",
      "26": "{count} MOD保存, CFG → {backup}",
      "27": "名前",
      "28": "作者",
      "29": "バージョン",
      "30": "言語",
      "31": "Steam ID",
      "32": "リンク",
      "33": "更新日",
      "34": "依存関係",
      "35": "KENSHI未検出",
      "36": "KENSHI起動エラー: {error}",
      "37": "設定未検出",
      "38": "MOD未検出",
      "39": "スキャンMOD押下",
      "40": "{count} 件並べ替え"
    }
  },

  "한국어": {
    "buttons": {
      "1": "모드 스캔",
      "2": "설정 불러오기",
      "3": "모드 정렬",
      "4": "설정 저장",
      "5": "지우기",
      "6": "내 게임",
      "7": "번역",
      "8": "켄시 시작",
      "9": "종료",
      "10": "작업 2",
      "11": "작업 3",
      "12": "작업 4",
      "13": "작업 5",
      "14": "뒤로"
    },
    "messages": {
      "1": "모드 목록이 삭제되었습니다",
      "2": "파일 삭제 오류",
      "3": "모드 스캔을 누르세요",
      "4": "폴더를 찾았습니다",
      "5": "로컬을 찾았습니다",
      "6": "KENSHI를 찾을 수 없습니다",
      "7": "올바른 위치에 설치하세요",
      "8": "설치",
      "9": "준비 완료",
      "10": "이전 모드 목록이 삭제되었습니다",
      "11": "스캔 완료: {count} 모드",
      "12": "정렬 완료",
      "13": "정렬 오류: {error}",
      "14": "{mod_name} 활성화/비활성화됨",
      "15": "오른쪽 클릭: {mod_name}이 MODS_ALL.JSON에 저장됨",
      "16": "오른쪽 클릭 저장 오류: {error}",
      "17": "프로필 {idx}이(가) 저장되었습니다",
      "18": "프로필 {idx}을(를) 찾을 수 없습니다",
      "19": "프로필 {idx}이(가) 비어 있습니다",
      "20": "프로필 {idx}에 모드가 없습니다",
      "21": "프로필 {idx}이(가) 로드되었습니다",
      "22": "저장할 모드가 없습니다",
      "23": "모드 구성 파일이 로드되었습니다",
      "24": "구성이 저장되었습니다 / 백업이 생성되었습니다",
      "25": "MODS.CFG에서 로드됨",
      "26": "{count}개의 모드가 저장되었습니다, CFG → {backup}",
      "27": "이름",
      "28": "작성자",
      "29": "버전",
      "30": "언어",
      "31": "Steam ID",
      "32": "링크",
      "33": "업데이트됨",
      "34": "의존성",
      "35": "KENSHI를 찾을 수 없습니다",
      "36": "KENSHI 실행 오류: {error}",
      "37": "설정을 찾을 수 없습니다",
      "38": "모드를 찾을 수 없습니다",
      "39": "모드 스캔을 누르세요",
      "40": "{count}개의 항목이 정렬되었습니다"
    }
  },

  "中文（简体）": {
    "buttons": {
      "1": "扫描Mod",
      "2": "加载配置",
      "3": "排序Mod",
      "4": "保存配置",
      "5": "清除",
      "6": "我的游戏",
      "7": "翻译",
      "8": "启动Kenshi",
      "9": "退出",
      "10": "操作2",
      "11": "操作3",
      "12": "操作4",
      "13": "操作5",
      "14": "返回"
    },
    "messages": {
      "1": "MOD列表已删除",
      "2": "删除文件错误",
      "3": "按扫描MOD",
      "4": "找到文件夹",
      "5": "找到本地",
      "6": "未找到KENSHI",
      "7": "安装到正确位置",
      "8": "安装",
      "9": "准备就绪",
      "10": "旧MOD列表已删除",
      "11": "扫描完成: {count} MOD",
      "12": "排序完成",
      "13": "排序错误: {error}",
      "14": "{mod_name} 启用/禁用",
      "15": "右键: {mod_name} 写入MODS_ALL.JSON",
      "16": "右键保存错误: {error}",
      "17": "配置文件{idx}已保存",
      "18": "配置文件{idx}未找到",
      "19": "配置文件{idx}为空",
      "20": "配置文件{idx}没有MOD",
      "21": "配置文件{idx}已加载",
      "22": "没有MOD可保存",
      "23": "MOD配置已加载",
      "24": "配置已保存 / 备份已创建",
      "25": "从MODS.CFG加载",
      "26": "保存了{count} MOD, CFG → {backup}",
      "27": "名称",
      "28": "作者",
      "29": "版本",
      "30": "语言",
      "31": "Steam ID",
      "32": "链接",
      "33": "已更新",
      "34": "依赖",
      "35": "未找到KENSHI",
      "36": "启动KENSHI错误: {error}",
      "37": "未找到设置",
      "38": "未找到MOD",
      "39": "按扫描MOD",
      "40": "排序了{count}条目"
    }
  }
}

# ================== СОЗДАНИЕ lang.json ==================
def ensure_lang_file():
    if not os.path.exists(LANG_FILE):
        with open(LANG_FILE, "w", encoding="utf-8") as f:
            json.dump(LANGS, f, ensure_ascii=False, indent=2)

# ================== SETTINGS ==================
def ensure_settings():
    default = {
        "shortcut": False,
        "steam": False,
        "local": False,
        "language": "English",
        "translator": "ChatGPT",
        "source_lang": "English",
        "target_lang": "Русский",
        "Profile-1": {"config": False, "mods": []},
        "Profile-2": {"config": False, "mods": []},
        "Profile-3": {"config": False, "mods": []},
    }
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)
    return default


def save_language(selected):
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = ensure_settings()
    else:
        data = ensure_settings()
    data["language"] = selected
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ================== ВСПЛЫВАЮЩЕЕ СООБЩЕНИЕ ==================
def show_message_window(message, color="#00FF00"):
    root = tk.Tk()
    root.overrideredirect(True)
    win_w, win_h = 380, 100
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    pos_x, pos_y = (screen_w - win_w)//2, (screen_h - win_h)//2
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

    DARK_BG = "#222222"
    canvas = tk.Canvas(root, width=win_w, height=win_h, highlightthickness=0, bg=DARK_BG)
    canvas.pack(fill="both", expand=True)
    border = 6
    canvas.create_line(0, 0, win_w, 0, fill=color, width=border)
    canvas.create_line(0, win_h, win_w, win_h, fill=color, width=border)
    canvas.create_text(win_w//2, win_h//2, text=message, fill="white", font=("Segoe UI", 12, "bold"))
    root.after(2000, root.destroy)
    root.mainloop()

# ================== ОКНО ВЫБОРА ЯЗЫКА ==================
def show_lang_selector():
    root = tk.Tk()
    root.overrideredirect(True)
    win_w, win_h = 380, 100
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    pos_x, pos_y = (screen_w - win_w)//2, (screen_h - win_h)//2
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

    DARK_BG = "#222222"
    BTN_BG = "#2b2b2b"
    BTN_ACTIVE = "#333333"
    BTN_FG = "white"
    RED_FG = "red"

    canvas = tk.Canvas(root, width=win_w, height=win_h, highlightthickness=0, bg=DARK_BG)
    canvas.pack(fill="both", expand=True)
    border = 6
    canvas.create_line(0, 0, win_w, 0, fill="#FF0000", width=border)
    canvas.create_line(0, win_h, win_w, win_h, fill="#FF0000", width=border)

    frame = tk.Frame(root, bg=DARK_BG)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    langs = list(LANGS.keys()) if LANGS else ["English"]
    selected_lang = tk.StringVar(value="English")
    dropdown_panel = None

    def toggle_dropdown():
        nonlocal dropdown_panel
        if dropdown_panel and dropdown_panel.winfo_exists():
            close_dropdown()
            return

        dropdown_panel = tk.Toplevel(root)
        dropdown_panel.overrideredirect(True)
        dropdown_panel.configure(bg=DARK_BG)
        dropdown_panel.lift()
        dropdown_panel.transient(root)

        root.update_idletasks()
        x = lang_btn.winfo_rootx()
        y = lang_btn.winfo_rooty() + lang_btn.winfo_height()
        w = lang_btn.winfo_width()
        dropdown_panel.geometry(f"{w}x0+{x}+{y}")

        text = tk.Text(dropdown_panel, bg=DARK_BG, fg=RED_FG,
                       wrap="none", borderwidth=0, highlightthickness=0,
                       font=("Segoe UI", 11, "bold"),
                       height=5, width=1, padx=5, pady=2,
                       cursor="arrow")
        text.pack(fill="both", expand=True)

        text.bind("<Button-1>", lambda e: "break")
        text.bind("<B1-Motion>", lambda e: "break")
        text.bind("<Double-Button-1>", lambda e: "break")

        for lang in langs:
            start_index = text.index("end-1c")
            centered_lang = lang.center(20)
            text.insert("end", f"{centered_lang}\n")
            end_index = text.index("end-1c")
            text.tag_add(lang, start_index, end_index)
            text.tag_config(lang, justify="center", foreground=RED_FG, font=("Segoe UI", 11, "bold"))
            text.tag_bind(lang, "<Enter>", lambda e, l=lang: text.tag_config(l, foreground="white"))
            text.tag_bind(lang, "<Leave>", lambda e, l=lang: text.tag_config(l, foreground=RED_FG))
            text.tag_bind(lang, "<Button-1>", lambda e, l=lang: select_lang(l))

        def on_mousewheel(event):
            text.yview_scroll(int(-1 * (event.delta / 120)), "units")

        text.bind("<MouseWheel>", on_mousewheel)
        text.config(state="disabled")

        text.update_idletasks()
        dropdown_panel.geometry(f"{w}x0+{x}+{y}")
        visible_height = min(int(text.count("1.0", "end", "ypixels")[0]), 5 * 28)
        animate_expand(dropdown_panel, target_h=visible_height, target_w=w, duration=250)

    def animate_expand(panel, target_h, target_w, duration=250):
        steps = 15
        delay = duration // steps
        for i in range(steps + 1):
            h = int(target_h * (i / steps))
            panel.after(i * delay, lambda hh=h: panel.geometry(f"{target_w}x{hh}+{lang_btn.winfo_rootx()}+{lang_btn.winfo_rooty() + lang_btn.winfo_height()}"))

    def animate_close(panel, duration=150):
        steps = 10
        delay = duration // steps
        for i in range(steps + 1):
            h = int(panel.winfo_height() * (1 - i / steps))
            panel.after(i * delay, lambda hh=h: panel.geometry(f"{lang_btn.winfo_width()}x{hh}+{lang_btn.winfo_rootx()}+{lang_btn.winfo_rooty() + lang_btn.winfo_height()}"))
        panel.after(duration + 30, panel.destroy)

    def select_lang(lang):
        selected_lang.set(lang)
        if dropdown_panel and dropdown_panel.winfo_exists():
            animate_close(dropdown_panel)

    def close_dropdown():
        if dropdown_panel and dropdown_panel.winfo_exists():
            animate_close(dropdown_panel)

    lang_btn = tk.Button(frame, textvariable=selected_lang,
                         bg=BTN_BG, fg="white",
                         activebackground=BTN_ACTIVE, activeforeground="white",
                         font=("Segoe UI", 11, "bold"),
                         relief="solid", bd=1, width=14, height=1,
                         command=toggle_dropdown)
    lang_btn.pack(pady=(0, 8))

    ok_btn = tk.Button(frame, text="OK", width=14, height=1,
                       bg=BTN_BG, fg=BTN_FG,
                       activebackground=BTN_ACTIVE, activeforeground=BTN_FG,
                       font=("Segoe UI", 11, "bold"),
                       relief="solid", bd=1,
                       command=lambda: on_ok(root, selected_lang.get()))
    ok_btn.pack()

    root.mainloop()


def on_ok(root, lang):
    save_language(lang)
    root.destroy()
    show_message_window(f"Language : {lang}", color="#00FF00")


# ================== MAIN ==================
if __name__ == "__main__":
    ensure_lang_file()
    ensure_settings()
    show_lang_selector()
