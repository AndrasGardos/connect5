from flask import Flask, request, jsonify
from board import Board

from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import sys

@app.route('/next-move', methods=['POST','GET'])
@cross_origin()
def nextMove():
    board = Board(request.json['board'])
    print(board, flush=True)

    best_move, best_score = board.minimax(maximizing = False, level = 2)
    board.rows[best_move[1]][best_move[0]] = -1 
    
    # Convert list of lists to list
    board_response = [item for sublist in board.rows for item in sublist]


    return jsonify(
        {
        "board": board_response
        })

if __name__ == '__main__':
    app.run(debug=True)

