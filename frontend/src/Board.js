import React, { useState, useEffect } from "react";
import "./Board.css";

import Box from "./Box";

function Board() {
  // First turn is human. humanTurn = true
  // Once the human puts a piece, humanTurn will be false
  // The useEffect will run, and the computer will put a piece
  // after the API returned, ueEffect will run again,
  // and humanTurn will be true again

  const [board, setBoard] = useState(Array(100).fill(0));
  const [humanTurn, setHumanTurn] = useState(false);

  function getNextMove() {
    // Send the board to the API
    fetch("http://127.0.0.1:5000/next-move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ board: board }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setBoard((prevBoard) => {
          let newBoard = data.board;
          console.log("newBoard:", newBoard);
          return newBoard;
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  useEffect(() => {
    if (!humanTurn) {
      // If this wasn't the human's move, we don't need to do anything
      console.log("Not human turn. (Computer turn)");
      setHumanTurn(true);
      return;
    }

    // Let's start the API call
    setHumanTurn(false);
    console.log("init API call");
    getNextMove();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [board]);

  function changeBox(index) {
    if (humanTurn === false) return;
    if (board[index] !== 0) return;

    let newBoard = [...board];
    newBoard[index] = 1;
    setBoard(newBoard);
  }

  return (
    <div
      className="board"
      style={{ backgroundColor: humanTurn ? "blue" : "red" }}
    >
      {board.map((state, index) => (
        <Box key={index} state={state} changeBox={() => changeBox(index)} />
      ))}
    </div>
  );
}

export default Board;
