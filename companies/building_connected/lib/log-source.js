'use strict'

const _ = require('lodash')
const faker = require('faker')
const P = require('bluebird')

function getNextPseudoRandomEntry(previousEntry) {
	return {
		date: previousEntry ?
			new Date(previousEntry.date.getTime() + 1000 * 60 * 60 * _.random(10) + _.random(1000 * 60)) :
			new Date(Date.now() - 1000 * 60 * 60 * 24 * _.random(40, 60)),
		msg: faker.company.catchPhrase(),
	}
}

exports.getSyncLogSource = function getSyncLogSource() {
	let drained = false
	let lastEntry = null

	return {
		pop() {
			lastEntry = getNextPseudoRandomEntry(lastEntry)
			if (lastEntry.date > new Date()) {
				drained = true
			}
			return drained ? false : lastEntry
		},
	}
}

exports.getAsyncLogSource = function getAsyncLogSource() {
	let drained = false
	let lastEntry = null
	let awaitingPromise = false

	return {
		popAsync() {
			if (awaitingPromise) {
				throw new Error('Cannot call popAsync while awaiting a promise')
			}
			awaitingPromise = true
			lastEntry = getNextPseudoRandomEntry(lastEntry)
			if (lastEntry.date > Date.now()) {
				drained = true
			}
			return P.delay(_.random(8)).then(() => {
				awaitingPromise = false
				return drained ? false : lastEntry
			})
		},
	}
}