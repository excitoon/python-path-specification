"""
This module provides :class:`.GitIgnoreSpec` which replicates
*.gitignore* behavior.
"""

from typing import (
	AnyStr,
	Callable,
	Iterable,
	TYPE_CHECKING,
	Union)

from .pathspec import (
	PathSpec)
from .pattern import (
	Pattern)
from .patterns.gitwildmatch import (
	GitWildMatchPattern)


class GitIgnoreSpec(PathSpec):
	"""
	The :class:`GitIgnoreSpec` class extends :class:`PathSpec` to
	replicate *.gitignore* behavior.
	"""

	def __eq__(self, other: 'Self') -> bool:
		"""
		Tests the equality of this gitignore-spec with *other*
		(:class:`GitIgnoreSpec`) by comparing their :attr:`~PathSpec.patterns`
		attributes. A non-:class:`GitIgnoreSpec` will not compare equal.
		"""
		if isinstance(other, GitIgnoreSpec):
			return super().__eq__(other)
		elif isinstance(other, PathSpec):
			return False
		else:
			return NotImplemented

	@classmethod
	def from_lines(
		cls,
		lines: Iterable[AnyStr],
		*,
		pattern_factory: Union[str, Callable[[AnyStr], Pattern], None] = None,
	) -> 'Self':
		"""
		Compiles the pattern lines.

		*lines* (:class:`~collections.abc.Iterable`) yields each uncompiled
		pattern (:class:`str`). This simply has to yield each line so it can
		be a :class:`io.TextIOBase` (e.g., from :func:`open` or
		:class:`io.StringIO`) or the result from :meth:`str.splitlines`.

		*pattern_factory* can be :data:`None`, the name of a registered
		pattern factory (:class:`str`), or a :class:`~collections.abc.Callable`
		used to compile patterns. The callable must accept an uncompiled
		pattern (:class:`str`) and return the compiled pattern (:class:`.Pattern`).
		Default is :data:`None` for :class:`.GitWildMatchPattern`).

		Returns the :class:`GitIgnoreSpec` instance.
		"""
		if pattern_factory is None:
			pattern_factory = GitWildMatchPattern

		self = super().from_lines(pattern_factory, lines)
		return self  # type: ignore


if TYPE_CHECKING:
	try:
		from typing import Self
	except ImportError:
		try:
			from typing_extensions import Self
		except ImportError:
			Self = GitIgnoreSpec
