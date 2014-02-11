from pylearn2.space import CompositeSpace
from pylearn2.utils.data_specs import is_flat_specs


class InfiniteDatasetIterator(object):
    """
    A thin wrapper around one of the mode iterators.

    Instead of working directly on a dataset's data, it acts on a `visiting
    order` list that the dataset provides.
    """
    def __init__(self, dataset, subset_iterator,
                 data_specs=None, return_tuple=False, convert=None):
        """
        .. todo::

            WRITEME
        """

        self._data_specs = data_specs
        self._dataset = dataset
        self._subset_iterator = subset_iterator
        self._return_tuple = return_tuple

        # Keep only the needed sources in self._raw_data.
        # Remember what source they correspond to in self._source
        assert is_flat_specs(data_specs)

        dataset_space, dataset_source = self._dataset.get_data_specs()
        assert is_flat_specs((dataset_space, dataset_source))

        # the dataset's data spec is either a single (space, source) pair,
        # or a pair of (non-nested CompositeSpace, non-nested tuple).
        # We could build a mapping and call flatten(..., return_tuple=True)
        # but simply putting spaces, sources and data in tuples is simpler.
        if not isinstance(dataset_source, tuple):
            dataset_source = (dataset_source,)

        if not isinstance(dataset_space, CompositeSpace):
            dataset_sub_spaces = (dataset_space,)
        else:
            dataset_sub_spaces = dataset_space.components
        assert len(dataset_source) == len(dataset_sub_spaces)

        # all_data = self._dataset.get_data()
        # if not isinstance(all_data, tuple):
        #     all_data = (all_data,)

        space, source = data_specs
        if not isinstance(source, tuple):
            source = (source,)
        if not isinstance(space, CompositeSpace):
            sub_spaces = (space,)
        else:
            sub_spaces = space.components
        assert len(source) == len(sub_spaces)

        # self._raw_data = tuple(all_data[dataset_source.index(s)]
        #                        for s in source)
        self._visiting_order = self._dataset.get_visiting_order()
        self._source = source

        if convert is None:
            self._convert = [None for s in source]
        else:
            assert len(convert) == len(source)
            self._convert = convert

        # for i, (so, sp) in enumerate(safe_zip(source, sub_spaces)):
        #     idx = dataset_source.index(so)
        #     dspace = dataset_sub_spaces[idx]

        #     init_fn = self._convert[i]
        #     fn = init_fn
        #     # Compose the functions
        #     needs_cast = not (np.dtype(config.floatX) ==
        #                       self._raw_data[i].dtype)
        #     if needs_cast:
        #         if fn is None:
        #             fn = lambda batch: numpy.cast[config.floatX](batch)
        #         else:
        #             fn = (lambda batch, fn_=fn:
        #                   numpy.cast[config.floatX](fn_(batch)))

        #     # If there is an init_fn, it is supposed to take
        #     # care of the formatting, and it should be an error
        #     # if it does not. If there was no init_fn, then
        #     # the iterator will try to format using the generic
        #     # space-formatting functions.
        #     needs_format = not init_fn and not sp == dspace
        #     if needs_format:
        #         # "dspace" and "sp" have to be passed as parameters
        #         # to lambda, in order to capture their current value,
        #         # otherwise they would change in the next iteration
        #         # of the loop.
        #         if fn is None:
        #             fn = (lambda batch, dspace=dspace, sp=sp:
        #                   dspace.np_format_as(batch, sp))
        #         else:
        #             fn = (lambda batch, dspace=dspace, sp=sp, fn_=fn:
        #                   dspace.np_format_as(fn_(batch), sp))

        #     self._convert[i] = fn

    def __iter__(self):
        """
        .. todo::

            WRITEME
        """
        return self

    def next(self):
        """
        .. todo::

            WRITEME
        """
        next_index = self._visiting_order[self._subset_iterator.next()]
        # TODO: handle fancy-index copies by allocating a buffer and
        # using numpy.take()

        rval = tuple(self._dataset.get(next_index))
                # fn(data[next_index]) if fn else data[next_index]
                # for data, fn in safe_zip(self._raw_data, self._convert))
        # rval = tuple(
        #         fn(data[next_index]) if fn else data[next_index]
        #         for data, fn in safe_zip(self._raw_data, self._convert))
        if not self._return_tuple and len(rval) == 1:
            rval, = rval
        return rval

    @property
    def batch_size(self):
        """
        .. todo::

            WRITEME
        """
        return self._subset_iterator.batch_size

    @property
    def num_batches(self):
        """
        .. todo::

            WRITEME
        """
        return self._subset_iterator.num_batches

    @property
    def num_examples(self):
        """
        .. todo::

            WRITEME
        """
        return self._subset_iterator.num_examples

    @property
    def uneven(self):
        """
        .. todo::

            WRITEME
        """
        return self._subset_iterator.uneven

    @property
    def stochastic(self):
        """
        .. todo::

            WRITEME
        """
        return self._subset_iterator.stochastic

