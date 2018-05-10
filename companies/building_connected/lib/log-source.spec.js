import test from 'ava'
import { getAsyncLogSource, getSyncLogSource } from './log-source'

test('should synchronously drain a log source', t => {
	const source = getSyncLogSource()
	let entry = source.pop()
	t.true(new Date() > entry.date)
	t.truthy(entry.msg)
})

test('should asynchronously drain a log source', async t => {
	const source = getAsyncLogSource()
	let entry = await source.popAsync()
	t.true(new Date() > entry.date)
	t.truthy(entry.msg)
	let nextEntry = await source.popAsync()
	t.true(nextEntry.date > entry.date)
	t.truthy(nextEntry.msg)
})

test('should throw error if popAsync called twice without first awaiting for result', async t => {
	const source = getAsyncLogSource()
	source.popAsync()
	t.throws(() => {
		source.popAsync()
	})
})