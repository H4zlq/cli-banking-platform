from databases.database import Database
from views.chooser_view import ChooserView


class Main:
    def run(self):
        # Create database and chooser view instances
        database = Database()
        chooser_view = ChooserView()

        # Initialize database
        database.init()

        # Run chooser view
        while True:
            chooser_view.main_menu()


if __name__ == "__main__":
    # Create main instance
    main = Main()

    # Run main
    main.run()
