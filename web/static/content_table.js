function $(v){
    return document.getElementById(v);
        }

var svg_none = '<path d="M 3 6 a 3 3 0 1 1 6 0 a 3 3 0 1 1 -6 0"></path>';
var svg_open = '<path d="m 1 4 l 6 6 l 0 -2.8 L 3.8 4 M 13 4 l -6 6 l 0 -2.8 L 10.2 4"></path>';
var svg_closed = '<path d="m 1 5 l 0 2 l 12 0 l 0 -2"></path>';

class CTPart {
    constructor(structure, elements){
        var id_ = structure[0];
        var name = structure[1];
        var raw_childs = structure[2];

        this.clicked = 0;
        this.should_display = 1;
        this.id = id_;
        this.name = name;

        var childs;
        var should_display_childs;
        if (raw_childs == null){
            childs = null;
            should_display_childs = 0;
        } else {
            childs = [];

            var index = 0;
            var limit = raw_childs.length;
            while (index < limit) {
                var element = raw_childs[index];
                var new_element = new CTPart(element, elements);
                childs.push(new_element);

                index = index+1;
                    }
            should_display_childs = 1;
                }

        this.childs = childs;
        this.should_display_childs = should_display_childs;
        elements[id_] = this;
            }

    entry_updated(entry_content){
        var should_display;
        if (this.name.indexOf(entry_content) == -1){
            should_display = 0;
        } else {
            should_display = 1;
                }

        var childs = this.childs;
        var should_display_childs = 0;

        if (childs != null){
            var index = 0;
            var limit = childs.length;

            var child;
            while (index < limit){
                child = childs[index];

                if (child.entry_updated(entry_content)){
                    should_display_childs = 1;
                    should_display = 1;
                        }

                index = index+1;
                    }
                }


        this.should_display = should_display;
        this.should_display_childs = should_display_childs;
        this.update_display_state();

        return should_display;
            }

    click(){
        var clicked;
        if (this.clicked){
            clicked = 0;
        } else {
            clicked = 1;
                    }

        this.clicked = clicked;
        this.update_display_state();
            }

    update_display_state(){
        var new_display;
        var new_display_childrens;
        var new_svg;

        if (this.should_display){
            var new_display = 'list-item';
            if (this.clicked){
                new_display_childrens = 'block';
                if (this.should_display_childs){
                    new_svg = svg_open;
                } else {
                    new_svg = svg_none;
                        }
            } else {
                new_display_childrens = 'none';
                if (this.should_display_childs){
                    new_svg = svg_closed;
                } else {
                    new_svg = svg_none;
                        }
                    }
        } else {
            new_display = 'none';
            new_svg = svg_none;
            new_display_childrens = 'none';
                }

        var id_ = this.id;
        var html_element;

        html_element = $(id_);
        html_element.style["display"] = new_display;

        if (this.childs != null){
            html_element = $(id_+'_c');
            html_element.style["display"] = new_display_childrens;

            html_element = $(id_+'_s');
            html_element.innerHTML = new_svg;
                }
            }
        }

class CT {
    constructor(raw_structures){
        this.entry_content = '';
        var elements = {};
        this.elements = elements;
        var structures = [];
        this.structures = structures;

        var index = 0;
        var limit = raw_structures.length;

        while (index < limit){
            var structure = raw_structures[index];
            var part = new CTPart(structure, elements);
            structures.push(part);

            index = index+1;
                }
            }

    click(id_) {
        this.elements[id_].click();
            }

    entry_update() {
        var entry_content = $('ct_input').value.toLowerCase();
        if (this.entry_content == entry_content) {
            return;
                }

        this.entry_content = entry_content;

        var structures = this.structures;
        var index = 0;
        var limit = structures.length;

        var structure;
        while (index < limit) {
            structure = structures[index];
            structure.entry_updated(entry_content);

            index = index+1;
                }

            }

    entry_clear() {
        $('ct_input').value = '';
        this.entry_update();
            }
        }

