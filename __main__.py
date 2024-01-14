from databases.database import Database
from views.chooser_view import ChooserView

if __name__ == "__main__":
    # Create database instance
    database = Database()

    # Initialize database
    database.init()

    # Create chooser view instance
    chooser_view = ChooserView()

    # Run chooser view
    while True:
        chooser_view.main_menu()
