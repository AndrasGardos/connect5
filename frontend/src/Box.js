export default function Box({ state, changeBox }) {
  function getClasses(state) {
    if (state === 0) return "box";
    if (state === 1) return "box box-x";
    if (state === -1) return "box box-o";
  }

  return (
    <div className={getClasses(state)} onClick={changeBox}>
      {state === 1 ? "X" : state === -1 ? "O" : ""}
    </div>
  );
}
