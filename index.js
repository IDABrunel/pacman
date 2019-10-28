require('./index.css')
const React = require('react')
const { useState } = require('react');
const ReactDOM = require('react-dom');

const LED_WIDTH = 32;
const LED_HEIGHT = 11;

const isValidPacmanLocation = () => {

}

const movementOperators = {
    fullyRandom: () => {
        const r = Math.random();
        // up, down, left, right
        if (r < 0.25) {
            return [1, 0, 0, 0];
        } else if (r < 0.5) {
            return [0, 1, 0, 0];
        } else if (r < 0.75) {
            return [0, 0, 1, 0];
        } else {
            return [0, 0, 0, 1];
        }
    }
}

const App = () => {
    const [pacmanLocation, setPacmanLocation] = useState([2, 13])
    const [boardState, setBoardState] = useState([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1],
    ])

    // setInterval(() => {
    //     const op = movementOperators.fullyRandom()
    //     if (op.reduce((prev, curr) => { return prev + curr}, 0) > 1) {
    //         throw new Error('Only one direction should be passed.')
    //     }
    //     const [up, down, left, right] = op;
    //     if (up) {
    //         setPacmanLocation([pacmanLocation[0] - 1, pacmanLocation[1]])
    //     }
    //     if (down) {
    //         setPacmanLocation([pacmanLocation[0] + 1, pacmanLocation[1]])
    //     }
    //     if (left) {
    //         setPacmanLocation([pacmanLocation[0], pacmanLocation[1] - 1])
    //     }
    //     if (right) {
    //         setPacmanLocation([pacmanLocation[0], pacmanLocation[1] + 1])
    //     }
    // }, 1000)

    const calculatedBoardState = boardState
    calculatedBoardState[pacmanLocation[0]][pacmanLocation[1]] = 2
    // setCalculatedBoardState(calculatedBoardState)
    console.log(calculatedBoardState)
    const [colourMappings, setColourMappings] = useState([
        // r, g, b
        [0, 0, 0],
        [48,79,254],
        [255,214,0]
    ])

    const renderRows = () => {
        const rows = []

        for (let y = 0; y < LED_HEIGHT; y++) {
            rows.push(<tr key={y}>{renderColumns(y)}</tr>)
        }

        return rows;
    }

    const renderColumns = (row) => {
        const rows = []

        for (let y = 0; y < LED_WIDTH; y++) {
            const [r, g, b] = colourMappings[calculatedBoardState[row][y]]
            rows.push(<td style={{backgroundColor: `rgb(${r}, ${g}, ${b})`}} key={y}>{calculatedBoardState[row][y]}</td>)
        }

        return rows;
    }


    return (
        <div>
            <table style={{
                margin: 'auto'
            }}>
                <tbody>{renderRows()}</tbody>
            </table>
        </div>
    )
}

ReactDOM.render(<App/>, document.getElementById('root'));
