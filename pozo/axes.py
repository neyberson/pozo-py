import warnings
import ood
import pozo
import pozo.renderers as pzr
import pozo.themes as pzt
import traceback


class Axis(ood.Item, pzt.Themeable):

    def set_name(self, name):
        warnings.warn("names are no longer used in pozo, use position. string selectors will search for mnemonics", DeprecationWarning)
        return super().set_name(name)

    def get_name(self):
        warnings.warn("names are no longer used in pozo, use position. string selectors will search for mnemonics", DeprecationWarning)
        return super().get_name()

    _type = "axis"
    _child_type = "trace"

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        for ar in args:
            self.add_traces(ar)

    def _check_types(self, *traces):
        accepted_types = (pozo.Trace)
        raw_return = []
        for trace in traces:
            if isinstance(trace, list):
                raw_return.extend(self._check_types(*trace))
            elif not isinstance(trace, accepted_types):
                raise TypeError(f"Axis.add_traces() only accepts pozo.Trace, or a single list of pozo.Trace, not {type(trace)}")
            else:
                raw_return.append(trace)
        return raw_return

    # add_items
    def add_traces(self, *traces, **kwargs):
        good_traces = self._check_types(*traces)
        super().add_items(*good_traces, **kwargs)
        return good_traces

    # get_items
    def get_traces(self, *selectors, **kwargs):
        good_selectors = []
        for selector in selectors:
            if isinstance(selector, str):
                good_selectors.append(pozo.HasLog(selector))
            else:
                good_selectors.append(selector)
        return super().get_items(*good_selectors, **kwargs)

    # get_item
    def get_trace(self, selector, **kwargs):
        if isinstance(selector, str):
            selector = pozo.HasLog(selector)
        return super().get_item(selector, **kwargs)

    # pop items
    def pop_traces(self,  *selectors, **kwargs):
        good_selectors = []
        for selector in selectors:
            if isinstance(selector, str):
                good_selectors.append(pozo.HasLog(selector))
            else:
                good_selectors.append(selector)
        return super().pop_items(*good_selectors, **kwargs)

    # what about whitelabelling all the other stuff
    def has_trace(self, selector):
        if isinstance(selector, str): # TODO all these transformations could be functions
            selector = pozo.HasLog(selector)
        return super().has_item(selector)

    def reorder_all_traces(self, order):
        good_selectors = []
        for selector in order:
            if isinstance(selector, str):
                good_selectors.append(pozo.HasLog(selector))
            else:
                good_selectors.append(selector)
        super().reorder_all_items(good_selectors)

    def move_traces(self, *selectors, **kwargs):
        good_selectors = []
        for selector in order:
            if isinstance(selector, str):
                good_selectors.append(pozo.HasLog(selector))
            else:
                good_selectors.append(selector)
        super().move_items(*good_selectors, **kwargs)

    def get_named_tree(self):
        result = []
        for el in self.get_traces():
            result.append(el.get_named_tree())
        return { "axis" : { self.name: result } }

    def get_theme(self):
        mnemonics = []
        for d in self.get_traces():
            mnemonics.append(d.get_mnemonic())
        context = { "type":"axis",
                   "name": self._name,
                   "mnemonics": mnemonics,
                   }
        return self._get_theme(context=context)
