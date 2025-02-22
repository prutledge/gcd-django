# -*- coding: utf-8 -*-


from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.contenttypes.forms import generic_inlineformset_factory

from apps.oi.models import OngoingReservation, ExternalLinkRevision
from apps.gcd.models import Series
from apps.stddata.forms import DateForm

# Some imports need a 'noqa' because we are only importing them to re-export
# through the forms module as a whole, which flake8 does not understand.
# The 'noqa' goes on the first line of the import, no matter where the
# apparently-unused import is in a multi-line import statement.
from .publisher import (get_publisher_revision_form,
                        get_indicia_publisher_revision_form,
                        get_brand_group_revision_form,
                        get_brand_revision_form,
                        get_brand_use_revision_form,
                        get_printer_revision_form,
                        get_indicia_printer_revision_form)
from .series import get_series_revision_form, get_series_bond_revision_form
from .issue import (    # noqa
    get_issue_revision_form, get_bulk_issue_revision_form,
    IssueRevisionFormSet, get_issue_revision_form_set_extra,
    PublisherCodeNumberFormSet)
from .story import (get_story_revision_form, get_biblio_revision_form,
                    get_reprint_revision_form, StoryRevisionFormSet,
                    StoryCharacterRevisionFormSet)
from .feature import (get_feature_revision_form,
                      get_feature_logo_revision_form,
                      get_feature_relation_revision_form)
from .character import (get_universe_revision_form,
                        get_character_revision_form, get_group_revision_form,
                        get_group_membership_revision_form,
                        get_character_relation_revision_form,
                        get_group_relation_revision_form,
                        GroupMembershipRevisionForm, CharacterRevisionFormSet)
from .image import (get_cover_revision_form,
                    UploadScanForm,
                    UploadVariantScanForm,
                    GatefoldScanForm,
                    UploadImageForm)
from .award import (get_award_revision_form,
                    get_received_award_revision_form,
                    ReceivedAwardRevisionForm)
from .creator import (    # noqa
    CreatorRevisionForm, CreatorArtInfluenceRevisionForm,
    CreatorMembershipRevisionForm, CreatorRevisionFormSet,
    CreatorNonComicWorkRevisionForm, CreatorRelationRevisionForm,
    CreatorSchoolRevisionForm, CreatorDegreeRevisionForm,
    CreatorSignatureRevisionForm,
    get_creator_art_influence_revision_form,
    get_creator_membership_revision_form, get_creator_revision_form,
    get_creator_non_comic_work_revision_form,
    get_creator_relation_revision_form, get_creator_signature_revision_form,
    get_creator_school_revision_form, get_creator_degree_revision_form)
from .support import (add_data_source_fields, init_data_source_fields,
                      _set_help_labels)


def get_revision_form(revision=None, model_name=None, **kwargs):
    if revision is not None and model_name is None:
        model_name = revision.source_name

    if model_name == 'publisher':
        source = None
        if revision is not None:
            source = revision.source
        return get_publisher_revision_form(source=source, **kwargs)

    if model_name == 'indicia_publisher':
        source = None
        if revision is not None:
            source = revision.source
        return get_indicia_publisher_revision_form(source=source, **kwargs)

    if model_name == 'brand_group':
        return get_brand_group_revision_form(**kwargs)

    if model_name == 'brand':
        return get_brand_revision_form(revision=revision, **kwargs)

    if model_name == 'brand_use':
        return get_brand_use_revision_form(**kwargs)

    if model_name == 'printer':
        source = None
        if revision is not None:
            source = revision.source
        return get_printer_revision_form(source=source, **kwargs)

    if model_name == 'indicia_printer':
        source = None
        if revision is not None:
            source = revision.source
        return get_indicia_printer_revision_form(source=source, **kwargs)

    if model_name == 'series':
        if revision is None:
            return get_series_revision_form(**kwargs)
        if 'publisher' not in kwargs:
            kwargs['publisher'] = revision.publisher
        return get_series_revision_form(revision=revision, **kwargs)

    if model_name == 'series_bond':
        return get_series_bond_revision_form(**kwargs)

    if model_name == 'issue':
        if revision is not None and 'publisher' not in kwargs:
            kwargs['publisher'] = revision.series.publisher
        return get_issue_revision_form(revision=revision, **kwargs)

    if model_name == 'story':
        return get_story_revision_form(revision, **kwargs)

    if model_name == 'feature':
        return get_feature_revision_form(revision, **kwargs)

    if model_name == 'feature_logo':
        return get_feature_logo_revision_form(revision, **kwargs)

    if model_name == 'feature_relation':
        return get_feature_relation_revision_form(revision, **kwargs)

    if model_name == 'universe':
        return get_universe_revision_form(revision, **kwargs)

    if model_name == 'character':
        return get_character_revision_form(revision, **kwargs)

    if model_name == 'character_relation':
        return get_character_relation_revision_form(revision, **kwargs)

    if model_name == 'group':
        return get_group_revision_form(revision, **kwargs)

    if model_name == 'group_relation':
        return get_group_relation_revision_form(revision, **kwargs)

    if model_name == 'group_membership':
        return get_group_membership_revision_form(revision, **kwargs)

    if model_name == 'biblio_entry':
        return get_biblio_revision_form(revision, **kwargs)

    if model_name == 'reprint':
        return get_reprint_revision_form(revision, **kwargs)

    if model_name in ['cover', 'image']:
        return get_cover_revision_form(revision, **kwargs)

    if model_name == 'award':
        return get_award_revision_form(revision, **kwargs)

    if model_name == 'received_award':
        return get_received_award_revision_form(revision, **kwargs)

    if model_name == 'creator':
        return get_creator_revision_form(revision, **kwargs)

    if model_name == 'creator_art_influence':
        return get_creator_art_influence_revision_form(revision, **kwargs)

    if model_name == 'creator_membership':
        return get_creator_membership_revision_form(revision, **kwargs)

    if model_name == 'creator_non_comic_work':
        return get_creator_non_comic_work_revision_form(revision, **kwargs)

    if model_name == 'creator_relation':
        return get_creator_relation_revision_form(revision, **kwargs)

    if model_name == 'creator_school':
        return get_creator_school_revision_form(revision, **kwargs)

    if model_name == 'creator_signature':
        return get_creator_signature_revision_form(revision, **kwargs)

    if model_name == 'creator_degree':
        return get_creator_degree_revision_form(revision, **kwargs)

    raise NotImplementedError


class ForeignKeyField(forms.IntegerField):
    def __init__(self, queryset, target_name=None, **kwargs):
        forms.IntegerField.__init__(self, **kwargs)
        self.queryset = queryset
        if target_name is not None:
            self.target_name = target_name

    def clean(self, value):
        id = forms.IntegerField.clean(self, value)
        if id is None:
            return id
        try:
            return self.queryset.get(id=id)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                "%d is not the ID of a valid %s" % (id, self.target_name))
        except MultipleObjectsReturned:
            raise forms.ValidationError(
                "%d matched multiple instances of %s" % (id, self.target_name))


class OngoingReservationForm(forms.ModelForm):
    class Meta:
        model = OngoingReservation
        fields = ('series',)
    series = ForeignKeyField(
        queryset=Series.objects.filter(ongoing_reservation__isnull=True,
                                       is_current=True),
        target_name='Available Series',
        help_text='The numeric database ID of a '
                  'series that does not already '
                  'have an ongoing reservation')


def get_date_revision_form(revision=None, user=None, date_help_links=[]):
    class RuntimeDateRevisionForm(DateRevisionForm):
        def __init__(self, *args, **kwargs):
            super(RuntimeDateRevisionForm, self).__init__(*args, **kwargs)
            if revision:
                init_data_source_fields(self.prefix, revision, self.fields)

        def as_table(self):
            if not user or user.indexer.show_wiki_links:
                _set_help_labels(self, date_help_links)
            return super(DateRevisionForm, self).as_table()

    return RuntimeDateRevisionForm


class DateRevisionForm(DateForm):
    def __init__(self, *args, **kwargs):
        super(DateRevisionForm, self).__init__(*args, **kwargs)
        add_data_source_fields(self, self.prefix)
        self.fields['date'].help_text = 'Enter date as YYYY-MM-DD or parts '\
          'thereof. A ? can be used in each part to indicate uncertainty.'

    def clean(self):
        cd = super(DateRevisionForm, self).clean()
        data_source_type = cd['%s_source_type' % self.prefix]
        data_source_description = cd['%s_source_description' % self.prefix]
        if data_source_type or data_source_description:
            if not data_source_type or not data_source_description:
                self.add_error(
                    '%s_source_description' % self.prefix,
                    'Source description and source type must both be set.')
        return cd


class ExternalLinkRevisionForm(forms.ModelForm):
    class Meta:
        model = ExternalLinkRevision
        fields = ['site', 'link']

    def clean(self):
        cd = self.cleaned_data
        if 'link' in cd and cd['link'] and 'site' in cd and \
           cd['site'].matching not in cd['link']:
            raise forms.ValidationError(
              ['Matching phrase "%s" from "%s" is not in "%s".' % (
                cd['site'].matching, cd['site'], cd['link'])])


ExternalLinkRevisionFormSet = generic_inlineformset_factory(
  ExternalLinkRevision, form=ExternalLinkRevisionForm,
  can_delete=True, extra=1)
