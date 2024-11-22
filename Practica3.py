import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QRadioButton
)
from nltk import CFG, ChartParser
from nltk.tree import Tree


class GrammarTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Árboles de Derivación y AST")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Widgets para la gramática y la expresión
        self.grammar_input = QTextEdit()
        self.grammar_input.setPlaceholderText("Introduce la gramática en formato BNF")
        layout.addWidget(QLabel("Gramática:"))
        layout.addWidget(self.grammar_input)

        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText("Introduce la expresión objetivo")
        layout.addWidget(QLabel("Expresión:"))
        layout.addWidget(self.expression_input)

        # Botones de derivación izquierda/derecha
        self.left_radio = QRadioButton("Derivación Izquierda")
        self.left_radio.setChecked(True)
        self.right_radio = QRadioButton("Derivación Derecha")
        layout.addWidget(self.left_radio)
        layout.addWidget(self.right_radio)

        # Botón para generar
        self.generate_button = QPushButton("Generar Árboles")
        self.generate_button.clicked.connect(self.generate_trees)
        layout.addWidget(self.generate_button)

        # Widget para mostrar resultados
        self.result_label = QLabel("Resultados:")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        # Configuración del layout principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_trees(self):
        # Obtener gramática y expresión
        grammar_text = self.grammar_input.toPlainText()
        expression = self.expression_input.toPlainText()

        try:
            grammar = CFG.fromstring(grammar_text)
            parser = ChartParser(grammar)

            # Generar derivaciones
            derivations = list(parser.parse(expression.split()))
            if not derivations:
                self.result_label.setText("No se pudo generar la derivación para la expresión.")
                return

            # Mostrar los árboles de derivación
            for tree in derivations:
                print("Árbol de derivación:")
                tree.pretty_print()  # Mostrar en la consola
                tree.draw()  # Mostrar en una ventana gráfica

            # Generar AST del primer árbol de derivación
            ast = self.generate_ast(derivations[0])
            print("Árbol Sintáctico Abstracto:")
            ast.pretty_print()

            self.result_label.setText("Árboles generados correctamente. Consulta la consola y la ventana gráfica para más detalles.")
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

    def generate_ast(self, tree: Tree) -> Tree:
        """
        Simplifica el árbol de derivación para generar el AST.
        Aquí puedes personalizar la lógica para eliminar nodos no esenciales.
        """
        if tree.height() <= 2:  # Nodo hoja o cercano
            return tree
        return Tree(tree.label(), [self.generate_ast(child) for child in tree if isinstance(child, Tree)])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GrammarTool()
    window.show()
    sys.exit(app.exec())
