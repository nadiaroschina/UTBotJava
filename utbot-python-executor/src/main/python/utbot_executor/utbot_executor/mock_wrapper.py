import logging
import types
import mock

from typing import Any, Dict, Optional
from contextlib import ExitStack


class MockWrapper:

    def __init__(self, mock_funcs_with_values: Optional[Dict[str, Any]] = None):
        self.mocks = list()
        if mock_funcs_with_values:
            for target, return_value in mock_funcs_with_values.items():
                self.mocks.append(mock.patch(target=target, new=mock.MagicMock(return_value=return_value)))
        logging.debug(f'MockWrapper initialized: {self.mocks=}, {mock_funcs_with_values=}')

    def wrap(self, f: types.FunctionType) -> types.FunctionType:

        def wrapped_func(*args, **kwargs):
            with ExitStack() as stack:
                for mock_context_manager in self.mocks:
                    stack.enter_context(mock_context_manager)
                return f(*args, **kwargs)

        return wrapped_func


class IntValueWrapper:
    def __init__(self):
        pass
