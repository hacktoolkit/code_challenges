import test from 'ava'
import Printer from './printer'

test('should throw when printing out of sync logs', t => {
  const printer = new Printer()
  const first = {
    msg: 'Foo',
    date: new Date(Date.now()),
  }
  const second = {
    msg: 'Bar',
    date: new Date(Date.now() + 1000),
  }
  t.throws(() => {
    printer.print(second)
    printer.print(first)
  })
})

test('should not throw when printing that are in sync logs', t => {
  const printer = new Printer()
  const first = {
    msg: 'Foo',
    date: new Date(Date.now()),
  }
  const second = {
    msg: 'Bar',
    date: new Date(Date.now() + 1000),
  }
  t.notThrows(() => {
    printer.print(first)
    printer.print(second)
  })
})
