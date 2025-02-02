#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the fake storage writer."""

import unittest

from plaso.containers import events
from plaso.containers import sessions
from plaso.containers import tasks
from plaso.lib import definitions
from plaso.storage.fake import writer as fake_writer

from tests.storage import test_lib
from tests.containers import test_lib as containers_test_lib


class FakeStorageWriterTest(test_lib.StorageTestCase):
  """Tests for the fake storage writer."""

  # pylint: disable=protected-access

  def testAddAttributeContainer(self):
    """Tests the AddAttributeContainer function."""
    event_data_stream = events.EventDataStream()

    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()

    number_of_containers = storage_writer._attribute_containers_counter[
        event_data_stream.CONTAINER_TYPE]
    self.assertEqual(number_of_containers, 0)

    storage_writer.AddAttributeContainer(event_data_stream)

    number_of_containers = storage_writer._attribute_containers_counter[
        event_data_stream.CONTAINER_TYPE]
    self.assertEqual(number_of_containers, 1)

    storage_writer.Close()

    with self.assertRaises(IOError):
      storage_writer.AddAttributeContainer(event_data_stream)

  # TODO: add tests for AddOrUpdateEventTag

  def testGetAttributeContainerByIdentifier(self):
    """Tests the GetAttributeContainerByIdentifier function."""
    event_data_stream = events.EventDataStream()

    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()

    storage_writer.AddAttributeContainer(event_data_stream)
    identifier = event_data_stream.GetIdentifier()

    container = storage_writer.GetAttributeContainerByIdentifier(
        event_data_stream.CONTAINER_TYPE, identifier)
    self.assertIsNotNone(container)

    identifier.sequence_number = 99

    container = storage_writer.GetAttributeContainerByIdentifier(
        event_data_stream.CONTAINER_TYPE, identifier)
    self.assertIsNone(container)

    storage_writer.Close()

  def testGetAttributeContainerByIndex(self):
    """Tests the GetAttributeContainerByIndex function."""
    event_data_stream = events.EventDataStream()

    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()

    container = storage_writer.GetAttributeContainerByIndex(
        event_data_stream.CONTAINER_TYPE, 0)
    self.assertIsNone(container)

    storage_writer.AddAttributeContainer(event_data_stream)

    container = storage_writer.GetAttributeContainerByIndex(
        event_data_stream.CONTAINER_TYPE, 0)
    self.assertIsNotNone(container)

    with self.assertRaises(IOError):
      storage_writer.GetAttributeContainerByIndex('bogus', 0)

    storage_writer.Close()

  # TODO: add tests for GetAttributeContainers

  # TODO: add tests for GetFirstWrittenEventSource and
  # GetNextWrittenEventSource.

  def testGetSortedEvents(self):
    """Tests the GetSortedEvents function."""
    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()

    for event, event_data, event_data_stream in (
        containers_test_lib.CreateEventsFromValues(self._TEST_EVENTS)):
      storage_writer.AddAttributeContainer(event_data_stream)

      event_data.SetEventDataStreamIdentifier(event_data_stream.GetIdentifier())
      storage_writer.AddAttributeContainer(event_data)

      event.SetEventDataIdentifier(event_data.GetIdentifier())
      storage_writer.AddAttributeContainer(event)

    test_events = list(storage_writer.GetSortedEvents())
    self.assertEqual(len(test_events), 4)

    storage_writer.Close()

    # TODO: add test with time range.

  def testOpenClose(self):
    """Tests the Open and Close functions."""
    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()
    storage_writer.Close()

    storage_writer.Open()
    storage_writer.Close()

    storage_writer = fake_writer.FakeStorageWriter(
        storage_type=definitions.STORAGE_TYPE_TASK)
    storage_writer.Open()
    storage_writer.Close()

    storage_writer.Open()

    with self.assertRaises(IOError):
      storage_writer.Open()

    storage_writer.Close()

    with self.assertRaises(IOError):
      storage_writer.Close()

  def testWriteSessionStartAndCompletion(self):
    """Tests the WriteSessionStart and WriteSessionCompletion functions."""
    session = sessions.Session()

    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()

    storage_writer.WriteSessionStart(session)
    storage_writer.WriteSessionCompletion(session)

    storage_writer.Close()

    with self.assertRaises(IOError):
      storage_writer.WriteSessionStart(session)

    with self.assertRaises(IOError):
      storage_writer.WriteSessionCompletion(session)

    storage_writer = fake_writer.FakeStorageWriter(
        storage_type=definitions.STORAGE_TYPE_TASK)
    storage_writer.Open()

    with self.assertRaises(IOError):
      storage_writer.WriteSessionStart(session)

    with self.assertRaises(IOError):
      storage_writer.WriteSessionCompletion(session)

    storage_writer.Close()

  def testWriteTaskStartAndCompletion(self):
    """Tests the WriteTaskStart and WriteTaskCompletion functions."""
    session = sessions.Session()
    task = tasks.Task(session_identifier=session.identifier)

    storage_writer = fake_writer.FakeStorageWriter(
        storage_type=definitions.STORAGE_TYPE_TASK)
    storage_writer.Open()

    storage_writer.WriteTaskStart(task)
    storage_writer.WriteTaskCompletion(task)

    storage_writer.Close()

    with self.assertRaises(IOError):
      storage_writer.WriteTaskStart(task)

    with self.assertRaises(IOError):
      storage_writer.WriteTaskCompletion(task)

    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()

    with self.assertRaises(IOError):
      storage_writer.WriteTaskStart(task)

    with self.assertRaises(IOError):
      storage_writer.WriteTaskCompletion(task)

    storage_writer.Close()


if __name__ == '__main__':
  unittest.main()
