'use strict'

const { getSyncLogSource, getAsyncLogSource } = require('./lib/log-source')
const Printer = require('./lib/printer')

// You can adjust this variable to see how your solutions perform under various "load"
const sourceCount = 10000

/**
 * Challenge Number 1!
 *
 * getSyncLogSource returns an object with a one method: pop() which will return a LogEntry.
 *
 * A LogEntry is simply an object of the form:
 * {
 * 		date: Date,
 * 		msg: String,
 * }
 *
 * All LogEntries from a given log source are guaranteed to be popped in chronological order.
 * Eventually a log source will end and return boolean false.
 *
 * Your job is simple: print the sorted merge of all LogEntries across `n` log sources.
 *
 * Call `printer.print(logEntry)` to print each entry of the merged output as they are ready.
 * This function will ensure that what you print is in fact in chronological order.
 * Call 'printer.done()' at the end to get a few stats on your solution!
 */

const syncLogSources = []
for (let i = 0; i < sourceCount; i++) {
	syncLogSources.push(getSyncLogSource())
}
require('./solution/sync-sorted-merge')(syncLogSources, new Printer())

/**
 * Challenge Number 2!
 *
 * Very similar to Challenge Number 1, except now you'll be using an object with a popAsync method
 * that returns a promise that resolves with a LogEntry, or boolean false once the log source
 * has ended.
 */

const asyncLogSources = []
for (let i = 0; i < sourceCount; i++) {
	asyncLogSources.push(getAsyncLogSource())
}
// require('./solution/async-sorted-merge')(asyncLogSources, new Printer())
