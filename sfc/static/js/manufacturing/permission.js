  var single = new SelectPure(".single-select", {
        options: [
          {
            label: "New York",
            value: 1,
            disabled: true,
          },
          {
            label: "San Francisco",
            value: 2,
          },
          {
            label: "Los Angeles",
            value: 3,
          },
        ],
        placeholder: "-Please select-",
        onChange: value => { console.log(value); },
        classNames: {
          select: "select-pure__select",
          dropdownShown: "select-pure__select--opened",
          multiselect: "select-pure__select--multiple",
          label: "select-pure__label",
          placeholder: "select-pure__placeholder",
          dropdown: "select-pure__options",
          option: "select-pure__option",
          autocompleteInput: "select-pure__autocomplete",
          selectedLabel: "select-pure__selected-label",
          selectedOption: "select-pure__option--selected",
          placeholderHidden: "select-pure__placeholder--hidden",
          optionHidden: "select-pure__option--hidden",
        }
      });
      var resetSingle = function() {
        single.reset();
      };

      var multi = new SelectPure(".multi-select", {
        options: [
          {
            label: "Developer",
            value: "1",
          },
          {
            label: "Operator",
            value: "2",
          },
          {
            label: "Administrator",
            value: "3",
          },

        ],
        multiple: true,
        icon: "fa fa-times",
        placeholder: "-Please select-",
        onChange: value => { console.log(value); },
        classNames: {
          select: "select-pure__select",
          dropdownShown: "select-pure__select--opened",
          multiselect: "select-pure__select--multiple",
          label: "select-pure__label",
          placeholder: "select-pure__placeholder",
          dropdown: "select-pure__options",
          option: "select-pure__option",
          autocompleteInput: "select-pure__autocomplete",
          selectedLabel: "select-pure__selected-label",
          selectedOption: "select-pure__option--selected",
          placeholderHidden: "select-pure__placeholder--hidden",
          optionHidden: "select-pure__option--hidden",
        }
      });
      var resetMulti = function() {
        multi.reset();
      };

      var customIcon = document.createElement('img');
      customIcon.src = './icon.svg';
      var customIconMulti = new SelectPure(".multi-select-custom", {
        options: [
          {
            label: "New York",
            value: "NY",
          },
          {
            label: "Washington",
            value: "WA",
          },
          {
            label: "California",
            value: "CA",
          },
          {
            label: "New Jersey",
            value: "NJ",
          },
          {
            label: "North Carolina",
            value: "NC",
          },
        ],
        value: ["NY", "CA"],
        multiple: true,
        inlineIcon: customIcon,
        onChange: value => { console.log(value); },
        classNames: {
          select: "select-pure__select",
          dropdownShown: "select-pure__select--opened",
          multiselect: "select-pure__select--multiple",
          label: "select-pure__label",
          placeholder: "select-pure__placeholder",
          dropdown: "select-pure__options",
          option: "select-pure__option",
          autocompleteInput: "select-pure__autocomplete",
          selectedLabel: "select-pure__selected-label",
          selectedOption: "select-pure__option--selected",
          placeholderHidden: "select-pure__placeholder--hidden",
          optionHidden: "select-pure__option--hidden",
        }
      });
      var resetCustomMulti = function() {
        customIconMulti.reset();
      };

      var autocomplete = new SelectPure(".autocomplete-select", {
        options: [
          {
            label: "Barbina",
            value: "ba",
          },
          {
            label: "Bigoli",
            value: "bg",
          },
          {
            label: "Bucatini",
            value: "bu",
          },
          {
            label: "Busiate",
            value: "bus",
          },
          {
            label: "Capellini",
            value: "cp",
          },
          {
            label: "Fedelini",
            value: "fe",
          },
          {
            label: "Maccheroni",
            value: "ma",
          },
          {
            label: "Spaghetti",
            value: "sp",
          },
        ],
        value: ["sp"],
        multiple: true,
        autocomplete: true,
        icon: "fa fa-times",
        onChange: value => { console.log(value); },
        classNames: {
          select: "select-pure__select",
          dropdownShown: "select-pure__select--opened",
          multiselect: "select-pure__select--multiple",
          label: "select-pure__label",
          placeholder: "select-pure__placeholder",
          dropdown: "select-pure__options",
          option: "select-pure__option",
          autocompleteInput: "select-pure__autocomplete",
          selectedLabel: "select-pure__selected-label",
          selectedOption: "select-pure__option--selected",
          placeholderHidden: "select-pure__placeholder--hidden",
          optionHidden: "select-pure__option--hidden",
        }
      });
      var resetAutocomplete = function() {
        autocomplete.reset();
      };