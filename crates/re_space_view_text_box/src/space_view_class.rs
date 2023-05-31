use egui::Label;
use re_viewer_context::{SpaceViewClassImpl, SpaceViewClassName, SpaceViewState, ViewerContext};

use super::scene_element::SceneTextBox;

// TODO(andreas): This should be a blueprint component.
#[derive(Clone, PartialEq, Eq)]
pub struct TextBoxSpaceViewState {
    monospace: bool,
    word_wrap: bool,
}

impl Default for TextBoxSpaceViewState {
    fn default() -> Self {
        Self {
            monospace: false,
            word_wrap: true,
        }
    }
}

impl SpaceViewState for TextBoxSpaceViewState {
    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn as_any_mut(&mut self) -> &mut dyn std::any::Any {
        self
    }
}

#[derive(Default)]
pub struct TextBoxSpaceView;

impl SpaceViewClassImpl for TextBoxSpaceView {
    type State = TextBoxSpaceViewState;
    type SceneElementTuple = (SceneTextBox,);

    fn name(&self) -> SpaceViewClassName {
        "Text Box".into()
    }

    fn icon(&self) -> &'static re_ui::Icon {
        &re_ui::icons::SPACE_VIEW_TEXTBOX
    }

    fn help_text(&self, _re_ui: &re_ui::ReUi) -> egui::WidgetText {
        "Displays text from a text entry components.".into()
    }

    fn new_scene(&self) -> Self::SceneElementTuple {
        (SceneTextBox::default(),)
    }

    fn selection_ui(
        &self,
        ctx: &mut ViewerContext<'_>,
        ui: &mut egui::Ui,
        state: &mut Self::State,
    ) {
        ctx.re_ui.selection_grid(ui, "text_config").show(ui, |ui| {
            ctx.re_ui.grid_left_hand_label(ui, "Text style");
            ui.vertical(|ui| {
                ui.radio_value(&mut state.monospace, false, "Proportional");
                ui.radio_value(&mut state.monospace, true, "Monospace");
                ui.checkbox(&mut state.word_wrap, "Word Wrap");
            });
            ui.end_row();
        });
    }

    fn ui(
        &self,
        _ctx: &mut ViewerContext<'_>,
        ui: &mut egui::Ui,
        state: &mut Self::State,
        scene_elements: Self::SceneElementTuple,
    ) {
        let scene = scene_elements.0;

        egui::Frame {
            inner_margin: re_ui::ReUi::view_padding().into(),
            ..egui::Frame::default()
        }
        .show(ui, |ui| {
            ui.with_layout(egui::Layout::top_down(egui::Align::LEFT), |ui| {
                egui::ScrollArea::both()
                    .auto_shrink([false, false])
                    .show(ui, |ui| {
                        // TODO(jleibs): better handling for multiple results
                        if scene.text_entries.len() == 1 {
                            let mut text = egui::RichText::new(&scene.text_entries[0].body);

                            if state.monospace {
                                text = text.monospace();
                            }

                            ui.add(Label::new(text).wrap(state.word_wrap));
                        } else {
                            ui.label(format!(
                                "Unexpected number of text entries: {}. Limit your query to 1.",
                                scene.text_entries.len()
                            ));
                        }
                    })
            })
            .response
        });
    }
}