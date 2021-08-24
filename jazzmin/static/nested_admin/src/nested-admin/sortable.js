'use strict';

const $ = require('jquery');
const regexQuote = require('./regexquote');
require('./jquery.ui.nestedsortable');

function updatePositions(prefix) {
    var position = 0,  // the value of the position formfield
        count = 1,     // The count displayed in stacked inline headers
        $group = $('#' + prefix + '-group'),
        groupData = $group.djnData(),
        fieldNames = groupData.fieldNames,
        // The field name on the fieldset which is a ForeignKey to the parent model
        groupFkName = groupData.formsetFkName,
        parentPkVal,
        [, parentPrefix, index] = prefix.match(/^(.*)\-(\d+)-[^\-]+(?:\-\d+)?$/) || [],
        sortableOptions = groupData.sortableOptions,
        sortableExcludes = (sortableOptions || {}).sortableExcludes || [];

    sortableExcludes.push(groupFkName);

    if (parentPrefix) {
        var $parentGroup = $('#' + parentPrefix + '-group');
        var parentFieldNames = $parentGroup.djnData('fieldNames');
        var parentPkFieldName = parentFieldNames.pk;
        var parentPkField = $parentGroup.filterDjangoField(parentPrefix, parentPkFieldName, index);
        parentPkVal = parentPkField.val();
    }

    if (groupFkName && typeof(parentPkVal) != 'undefined') {
        $group.filterDjangoField(prefix, groupFkName).val(parentPkVal).trigger('change');
    }

    $group.find('.djn-inline-form').each(function() {
        if (!this.id || this.id.substr(-6) == '-empty') {
            return true; // Same as continue
        }
        var regex = new RegExp('^(?:id_)?' + regexQuote(prefix) + '\\-\\d+$');

        if (!this.id.match(regex)) {
            return true;
        }
        // Cache jQuery object
        var $this = $(this),
            [formPrefix, index] = $this.djangoPrefixIndex() || [null, null],
            namePrefix = formPrefix + '-' + index + '-';

        if (!formPrefix) {
            return;
        }

        // Set header position for stacked inlines in Django 1.9+
        var $inlineLabel = $this.find('.card > .card-header > .row > h3 > .inline_label');
        if ($inlineLabel.length) {
            $inlineLabel.html($inlineLabel.html().replace(/(\(\d\))/g, '(' + count + ')'));
        }
        count++;

        // Set collapse id for cards
        var $cardHeader = $this.find('.card > .collapsible-header');
        if ($cardHeader.length) {
            $cardHeader.attr('data-target', '#' + namePrefix + 'tab');
        }

        var $panelCollapse = $this.find('.card > .panel-collapse');
        if ($panelCollapse.length) {
            $panelCollapse.attr('id', namePrefix + 'tab');
        }

        var $fields = $this.djangoFormField('*'),
            $positionField,
            setPosition = false;

        // position is being updated if
        // a) the field has a value
        // b) if the field is not exluded with sortable_excludes (e.g. with default values)
        $fields.each(function() {
            var $field = $(this);
            if (!$field.is(':input[type!=radio][type!=checkbox],input:checked')) {
                return;
            }
            var hasValue = $field.val() || ($field.attr('type') == 'file' && $field.siblings('a').length),
                fieldName = $field.attr('name').substring(namePrefix.length);
            if (fieldName == fieldNames.position) {
                $positionField = $field;
            }
            if (hasValue && $.inArray(fieldName, sortableExcludes) === -1) {
                setPosition = true;
            }
        });

        if (!setPosition || !$positionField) {
            return;
        }

        $positionField.val(position).trigger('change');
        position++;
    });
}

function createSortable($group) {
    const isPolymorphic = $group.is('.djn-is-polymorphic');
    return $group.find('> .djn-items, > .djn-fieldset > .djn-items, > .tabular > .module > .djn-items').nestedSortable({
        handle: [
            '> h3.djn-drag-handler',
            '> .djn-tools .drag-handler',
            '> .djn-td > .djn-tools .djn-drag-handler',
            '> .djn-tr > .is-sortable > .djn-drag-handler',
            '> .djn-tr > .grp-tools-container .djn-drag-handler'
        ].join(', '),
        /**
         * items: The selector for ONLY the items underneath a given
         *        container at that level. Not to be confused with
         *        listItemSelector, which is the selector for all list
         *        items in the nestedSortable
         */
        items: '> .djn-item',
        forcePlaceholderSize: true,
        placeholder: {
            element: function($currentItem) {
                var el = $(document.createElement($currentItem[0].nodeName))
                    .addClass($currentItem[0].className + ' ui-sortable-placeholder')
                    .removeClass('ui-sortable-helper')[0];

                if ($currentItem.is('.djn-tbody')) {
                    var $originalTr = $currentItem.children('.djn-tr').eq(0);
                    var trTagName = $originalTr.prop('tagName').toLowerCase();
                    var $tr = $(`<${trTagName}></${trTagName}>`);
                    $tr.addClass($originalTr.attr('class'));
                    var $originalTd = $originalTr.children('.djn-td').eq(0);
                    var tdTagName = $originalTd.prop('tagName').toLowerCase();
                    var numColumns = 0;
                    $originalTr.children('.djn-td').each(function(i, td) {
                        numColumns += parseInt($(td).attr('colspan'), 10) || 1;
                    });
                    $tr.append($(`<${tdTagName} colspan="${numColumns}" class="djn-td grp-td"></${tdTagName}>`));
                    el.appendChild($tr[0]);
                }

                return el;
            },
            update: function(instance, $placeholder) {
                var $currItem = instance.currentItem;
                if (!$currItem) {
                    return;
                }
                var opts = instance.options;
                // 1. If a className is set as 'placeholder option, we
                //    don't force sizes - the class is responsible for that
                // 2. The option 'forcePlaceholderSize can be enabled to
                //    force it even if a class name is specified
                if (opts.className && !opts.forcePlaceholderSize) return;

                if ($placeholder.is('.djn-tbody')) {
                    // debugger;
                    $placeholder = $placeholder.children('.djn-tr').eq(0).children('.djn-td').eq(0);
                }

                // If the element doesn't have a actual height by itself
                // (without styles coming from a stylesheet), it receives
                // the inline height from the dragged item
                if (!$placeholder.height()) {
                    var innerHeight = $currItem.innerHeight(),
                        paddingTop = parseInt($currItem.css('paddingTop') || 0, 10),
                        paddingBottom = parseInt($currItem.css('paddingBottom') || 0, 10);
                    $placeholder.height(innerHeight - paddingTop - paddingBottom);
                }
                if (!$placeholder.width()) {
                    var innerWidth = $currItem.innerWidth(),
                        paddingLeft = parseInt($currItem.css('paddingLeft') || 0, 10),
                        paddingRight = parseInt($currItem.css('paddingRight') || 0, 10);
                    $placeholder.width(innerWidth - paddingLeft - paddingRight);
                }
            }
        },
        helper: 'clone',
        opacity: 0.6,
        maxLevels: 0,
        connectWith: '.djn-items',
        tolerance: 'intersection',
        // Don't allow dragging beneath an inline that is marked for deletion
        isAllowed: function(currentItem, parentItem) {
            if (parentItem && parentItem.hasClass('predelete')) {
                return false;
            }
            const $parentGroup = parentItem.closest('.djn-group');
            const parentModel = $parentGroup.data('inlineModel');
            const childModels = $parentGroup.djnData('childModels');
            const currentModel = currentItem.data('inlineModel');
            const isPolymorphicChild = (childModels && childModels.indexOf(currentModel) !== -1);
            if (currentModel !== parentModel && !isPolymorphicChild) {
                return false;
            }
            return true;
        },
        // fixedNestingDepth: not a standard ui.sortable parameter.
        // Prevents dragging items up or down levels
        fixedNestingDepth: true,
        // The selector for ALL list containers in the nested sortable.
        containerElementSelector: '.djn-items',
        // The selector for ALL list items in the nested sortable.
        listItemSelector: '.djn-item',
        start: function(event, ui) {
            ui.item.addClass('djn-item-dragging');
            ui.item.show();
        },
        stop: function(event, ui) {
            ui.item.removeClass('djn-item-dragging');
        },
        /**
         * Triggered when a sortable is dropped into a container
         */
        receive: function(event, ui) {
            var $inline = $(this).closest('.djn-group');
            $inline.djangoFormset().spliceInto(ui.item);
            updatePositions(ui.item.djangoFormsetPrefix());
        },
        update: function(event, ui) {
            // Ensure that <div class='djn-item djn-no-drag'/>
            // is the first child of the djn-items. If there
            // is another <div class='djn-item'/> before the
            // .do-not-drag element then the drag-and-drop placeholder
            // margins don't work correctly.
            var $nextItem = ui.item.nextAll('.djn-item').first();
            if ($nextItem.is('.djn-no-drag,.djn-thead')) {
                var nextItem = $nextItem[0];
                var parent = nextItem.parentNode;
                parent.insertBefore(nextItem, parent.firstChild);
            }
            var groupId = $(event.target).closest('.djn-group').attr('id'),
                $form = ui.item,
                $parentGroup = $form.closest('#' + groupId);
            if ($form.data('updateOperation') == 'removed') {
                $form.removeAttr('data-update-operation');
            } else if (!$parentGroup.length) {
                $form.attr('data-update-operation', 'removed');
            }
            updatePositions($form.djangoFormsetPrefix());
            $(document).trigger('djnesting:mutate', [$('#' + $form.djangoFormsetPrefix() + '-group')]);
        }
    });
}

module.exports = {updatePositions, createSortable};
