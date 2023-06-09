from pyi18n import PyI18n

i18n = PyI18n(("en", "ru", "uk", "es", "pt"
               , "fr"), load_path="locales/")
_: callable = i18n.gettext
