'use strict'

module.exports = (logSources, printer) => {
    const buffer = {}; // holds already-popped items before they are consumed

    const advanceLogSource = (i) => {
        const logSource = logSources[i];
        const value = logSource.pop();
        buffer[i] = value;
    }

    // take the first element from each log source first
    logSources.forEach(function(logSource, i) {
        advanceLogSource(i);
    });

    const getNextLogEntry = () => {
        // the next log entry must be currently in the buffer (the first in each queue)
        var bestSoFar = null;
        var bestSoFarIndex = null;

        for (let i=0; i < logSources.length; ++i) {
            let value = buffer[i];
            if (value !== false) {
                if (bestSoFar === null || (bestSoFar && value.date < bestSoFar.date)) {
                    bestSoFar = value;
                    bestSoFarIndex = i;
                }
            }
        }

        if (bestSoFarIndex !== null) {
            advanceLogSource(bestSoFarIndex);
        }

        return bestSoFar;
    }

    let loops = 0;
    while (true) {
        let logEntry = getNextLogEntry();
        if (logEntry) {
            printer.print(logEntry);
        } else {
            break;
        }
    }
    printer.done();
}
