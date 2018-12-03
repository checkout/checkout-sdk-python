from checkout_sdk.payments.responses.card_source import CardSource

source_classes = {
    'card': CardSource
    # s APM will follow here
}


class SourceFactory:
    @classmethod
    def create_source(cls, source):
        if source is not None:
            source_cls = source_classes.get(source.get('type'), None)
            if source_cls is not None:
                return source_cls(source)

        return None
