// DO NOT EDIT!: This file was auto-generated by crates/re_types_builder/src/codegen/rust/api.rs:165.

#![allow(trivial_numeric_casts)]
#![allow(unused_parens)]
#![allow(clippy::clone_on_copy)]
#![allow(clippy::iter_on_single_items)]
#![allow(clippy::map_flatten)]
#![allow(clippy::match_wildcard_for_single_variants)]
#![allow(clippy::needless_question_mark)]
#![allow(clippy::redundant_closure)]
#![allow(clippy::too_many_arguments)]
#![allow(clippy::too_many_lines)]
#![allow(clippy::unnecessary_cast)]

/// A batch of line strips with positions and optional colors, radii, labels, etc.
///
/// ## Example
///
/// Many strips:
/// ```ignore
/// //! Log a batch of 2d line strips.
///
/// use rerun::{
///    archetypes::LineStrips2D, components::Rect2D, datatypes::Vec4D, MsgSender,
///    RecordingStreamBuilder,
/// };
///
/// fn main() -> Result<(), Box<dyn std::error::Error>> {
///    let (rec_stream, storage) =
///        RecordingStreamBuilder::new("rerun_example_line_strip2d").memory()?;
///
///    let strip1 = [[0., 0.], [2., 1.], [4., -1.], [6., 0.]];
///    #[rustfmt::skip]
///    let strip2 = [[0., 3.], [1., 4.], [2., 2.], [3., 4.], [4., 2.], [5., 4.], [6., 3.]];
///    MsgSender::from_archetype(
///        "strips",
///        &LineStrips2D::new([strip1.to_vec(), strip2.to_vec()])
///            .with_colors([0xFF0000FF, 0x00FF00FF])
///            .with_radii([0.025, 0.005])
///            .with_labels(["one strip here", "and one strip there" /**/]),
///    )?
///    .send(&rec_stream)?;
///
///    // Log an extra rect to set the view bounds
///    MsgSender::new("bounds")
///        .with_component(&[Rect2D::XCYCWH(Vec4D([3.0, 1.5, 8.0, 9.0]).into())])?
///        .send(&rec_stream)?;
///
///    rerun::native_viewer::show(storage.take())?;
///    Ok(())
/// }
/// ```
///
/// Many individual segments:
/// ```ignore
/// //! Log a couple 2D line segments using 2D line strips.
///
/// use rerun::{
///    archetypes::LineStrips2D, components::Rect2D, datatypes::Vec4D, MsgSender,
///    RecordingStreamBuilder,
/// };
///
/// fn main() -> Result<(), Box<dyn std::error::Error>> {
///    let (rec_stream, storage) =
///        RecordingStreamBuilder::new("rerun_example_line_segments2d").memory()?;
///
///    let points = [[0., 0.], [2., 1.], [4., -1.], [6., 0.]];
///    MsgSender::from_archetype("segments", &LineStrips2D::new(points.chunks(2)))?
///        .send(&rec_stream)?;
///
///    // Log an extra rect to set the view bounds
///    MsgSender::new("bounds")
///        .with_component(&[Rect2D::XCYCWH(Vec4D([3.0, 0.0, 8.0, 6.0]).into())])?
///        .send(&rec_stream)?;
///
///    rerun::native_viewer::show(storage.take())?;
///    Ok(())
/// }
/// ```
#[derive(Clone, Debug, PartialEq)]
pub struct LineStrips2D {
    /// All the actual 2D line strips that make up the batch.
    pub strips: Vec<crate::components::LineStrip2D>,

    /// Optional radii for the line strips.
    pub radii: Option<Vec<crate::components::Radius>>,

    /// Optional colors for the line strips.
    pub colors: Option<Vec<crate::components::Color>>,

    /// Optional text labels for the line strips.
    pub labels: Option<Vec<crate::components::Label>>,

    /// An optional floating point value that specifies the 2D drawing order of each line strip.
    /// Objects with higher values are drawn on top of those with lower values.
    ///
    /// The default for 2D lines is 20.0.
    pub draw_order: Option<crate::components::DrawOrder>,

    /// Optional `ClassId`s for the lines.
    ///
    /// The class ID provides colors and labels if not specified explicitly.
    pub class_ids: Option<Vec<crate::components::ClassId>>,

    /// Unique identifiers for each individual line strip in the batch.
    pub instance_keys: Option<Vec<crate::components::InstanceKey>>,
}

static REQUIRED_COMPONENTS: once_cell::sync::Lazy<[crate::ComponentName; 1usize]> =
    once_cell::sync::Lazy::new(|| ["rerun.linestrip2d".into()]);

static RECOMMENDED_COMPONENTS: once_cell::sync::Lazy<[crate::ComponentName; 2usize]> =
    once_cell::sync::Lazy::new(|| ["rerun.radius".into(), "rerun.colorrgba".into()]);

static OPTIONAL_COMPONENTS: once_cell::sync::Lazy<[crate::ComponentName; 4usize]> =
    once_cell::sync::Lazy::new(|| {
        [
            "rerun.label".into(),
            "rerun.draw_order".into(),
            "rerun.components.ClassId".into(),
            "rerun.instance_key".into(),
        ]
    });

static ALL_COMPONENTS: once_cell::sync::Lazy<[crate::ComponentName; 7usize]> =
    once_cell::sync::Lazy::new(|| {
        [
            "rerun.linestrip2d".into(),
            "rerun.radius".into(),
            "rerun.colorrgba".into(),
            "rerun.label".into(),
            "rerun.draw_order".into(),
            "rerun.components.ClassId".into(),
            "rerun.instance_key".into(),
        ]
    });

impl LineStrips2D {
    pub const NUM_COMPONENTS: usize = 7usize;
}

impl crate::Archetype for LineStrips2D {
    #[inline]
    fn name() -> crate::ArchetypeName {
        "rerun.archetypes.LineStrips2D".into()
    }

    #[inline]
    fn required_components() -> ::std::borrow::Cow<'static, [crate::ComponentName]> {
        REQUIRED_COMPONENTS.as_slice().into()
    }

    #[inline]
    fn recommended_components() -> ::std::borrow::Cow<'static, [crate::ComponentName]> {
        RECOMMENDED_COMPONENTS.as_slice().into()
    }

    #[inline]
    fn optional_components() -> ::std::borrow::Cow<'static, [crate::ComponentName]> {
        OPTIONAL_COMPONENTS.as_slice().into()
    }

    #[inline]
    fn all_components() -> ::std::borrow::Cow<'static, [crate::ComponentName]> {
        ALL_COMPONENTS.as_slice().into()
    }

    #[inline]
    fn indicator_component() -> crate::ComponentName {
        "rerun.components.LineStrips2DIndicator".into()
    }

    #[inline]
    fn num_instances(&self) -> usize {
        self.strips.len()
    }

    fn as_component_lists(&self) -> Vec<&dyn crate::ComponentList> {
        [
            Some(&self.strips as &dyn crate::ComponentList),
            self.radii
                .as_ref()
                .map(|comp_list| comp_list as &dyn crate::ComponentList),
            self.colors
                .as_ref()
                .map(|comp_list| comp_list as &dyn crate::ComponentList),
            self.labels
                .as_ref()
                .map(|comp_list| comp_list as &dyn crate::ComponentList),
            self.draw_order
                .as_ref()
                .map(|comp| comp as &dyn crate::ComponentList),
            self.class_ids
                .as_ref()
                .map(|comp_list| comp_list as &dyn crate::ComponentList),
            self.instance_keys
                .as_ref()
                .map(|comp_list| comp_list as &dyn crate::ComponentList),
        ]
        .into_iter()
        .flatten()
        .collect()
    }

    #[inline]
    fn try_to_arrow(
        &self,
    ) -> crate::SerializationResult<
        Vec<(::arrow2::datatypes::Field, Box<dyn ::arrow2::array::Array>)>,
    > {
        use crate::{Loggable as _, ResultExt as _};
        Ok([
            {
                Some({
                    let array = <crate::components::LineStrip2D>::try_to_arrow(self.strips.iter());
                    array.map(|array| {
                        let datatype = ::arrow2::datatypes::DataType::Extension(
                            "rerun.components.LineStrip2D".into(),
                            Box::new(array.data_type().clone()),
                            Some("rerun.linestrip2d".into()),
                        );
                        (
                            ::arrow2::datatypes::Field::new("strips", datatype, false),
                            array,
                        )
                    })
                })
                .transpose()
                .with_context("rerun.archetypes.LineStrips2D#strips")?
            },
            {
                self.radii
                    .as_ref()
                    .map(|many| {
                        let array = <crate::components::Radius>::try_to_arrow(many.iter());
                        array.map(|array| {
                            let datatype = ::arrow2::datatypes::DataType::Extension(
                                "rerun.components.Radius".into(),
                                Box::new(array.data_type().clone()),
                                Some("rerun.radius".into()),
                            );
                            (
                                ::arrow2::datatypes::Field::new("radii", datatype, false),
                                array,
                            )
                        })
                    })
                    .transpose()
                    .with_context("rerun.archetypes.LineStrips2D#radii")?
            },
            {
                self.colors
                    .as_ref()
                    .map(|many| {
                        let array = <crate::components::Color>::try_to_arrow(many.iter());
                        array.map(|array| {
                            let datatype = ::arrow2::datatypes::DataType::Extension(
                                "rerun.components.Color".into(),
                                Box::new(array.data_type().clone()),
                                Some("rerun.colorrgba".into()),
                            );
                            (
                                ::arrow2::datatypes::Field::new("colors", datatype, false),
                                array,
                            )
                        })
                    })
                    .transpose()
                    .with_context("rerun.archetypes.LineStrips2D#colors")?
            },
            {
                self.labels
                    .as_ref()
                    .map(|many| {
                        let array = <crate::components::Label>::try_to_arrow(many.iter());
                        array.map(|array| {
                            let datatype = ::arrow2::datatypes::DataType::Extension(
                                "rerun.components.Label".into(),
                                Box::new(array.data_type().clone()),
                                Some("rerun.label".into()),
                            );
                            (
                                ::arrow2::datatypes::Field::new("labels", datatype, false),
                                array,
                            )
                        })
                    })
                    .transpose()
                    .with_context("rerun.archetypes.LineStrips2D#labels")?
            },
            {
                self.draw_order
                    .as_ref()
                    .map(|single| {
                        let array = <crate::components::DrawOrder>::try_to_arrow([single]);
                        array.map(|array| {
                            let datatype = ::arrow2::datatypes::DataType::Extension(
                                "rerun.components.DrawOrder".into(),
                                Box::new(array.data_type().clone()),
                                Some("rerun.draw_order".into()),
                            );
                            (
                                ::arrow2::datatypes::Field::new("draw_order", datatype, false),
                                array,
                            )
                        })
                    })
                    .transpose()
                    .with_context("rerun.archetypes.LineStrips2D#draw_order")?
            },
            {
                self.class_ids
                    .as_ref()
                    .map(|many| {
                        let array = <crate::components::ClassId>::try_to_arrow(many.iter());
                        array.map(|array| {
                            let datatype = ::arrow2::datatypes::DataType::Extension(
                                "rerun.components.ClassId".into(),
                                Box::new(array.data_type().clone()),
                                Some("rerun.components.ClassId".into()),
                            );
                            (
                                ::arrow2::datatypes::Field::new("class_ids", datatype, false),
                                array,
                            )
                        })
                    })
                    .transpose()
                    .with_context("rerun.archetypes.LineStrips2D#class_ids")?
            },
            {
                self.instance_keys
                    .as_ref()
                    .map(|many| {
                        let array = <crate::components::InstanceKey>::try_to_arrow(many.iter());
                        array.map(|array| {
                            let datatype = ::arrow2::datatypes::DataType::Extension(
                                "rerun.components.InstanceKey".into(),
                                Box::new(array.data_type().clone()),
                                Some("rerun.instance_key".into()),
                            );
                            (
                                ::arrow2::datatypes::Field::new("instance_keys", datatype, false),
                                array,
                            )
                        })
                    })
                    .transpose()
                    .with_context("rerun.archetypes.LineStrips2D#instance_keys")?
            },
            {
                let datatype = ::arrow2::datatypes::DataType::Extension(
                    "rerun.components.LineStrips2DIndicator".to_owned(),
                    Box::new(::arrow2::datatypes::DataType::Null),
                    Some("rerun.components.LineStrips2DIndicator".to_owned()),
                );
                let array = ::arrow2::array::NullArray::new(
                    datatype.to_logical_type().clone(),
                    self.num_instances(),
                )
                .boxed();
                Some((
                    ::arrow2::datatypes::Field::new(
                        "rerun.components.LineStrips2DIndicator",
                        datatype,
                        false,
                    ),
                    array,
                ))
            },
        ]
        .into_iter()
        .flatten()
        .collect())
    }

    #[inline]
    fn try_from_arrow(
        arrow_data: impl IntoIterator<
            Item = (::arrow2::datatypes::Field, Box<dyn ::arrow2::array::Array>),
        >,
    ) -> crate::DeserializationResult<Self> {
        use crate::{Loggable as _, ResultExt as _};
        let arrays_by_name: ::std::collections::HashMap<_, _> = arrow_data
            .into_iter()
            .map(|(field, array)| (field.name, array))
            .collect();
        let strips = {
            let array = arrays_by_name
                .get("strips")
                .ok_or_else(crate::DeserializationError::missing_data)
                .with_context("rerun.archetypes.LineStrips2D#strips")?;
            <crate::components::LineStrip2D>::try_from_arrow_opt(&**array)
                .with_context("rerun.archetypes.LineStrips2D#strips")?
                .into_iter()
                .map(|v| v.ok_or_else(crate::DeserializationError::missing_data))
                .collect::<crate::DeserializationResult<Vec<_>>>()
                .with_context("rerun.archetypes.LineStrips2D#strips")?
        };
        let radii = if let Some(array) = arrays_by_name.get("radii") {
            Some({
                <crate::components::Radius>::try_from_arrow_opt(&**array)
                    .with_context("rerun.archetypes.LineStrips2D#radii")?
                    .into_iter()
                    .map(|v| v.ok_or_else(crate::DeserializationError::missing_data))
                    .collect::<crate::DeserializationResult<Vec<_>>>()
                    .with_context("rerun.archetypes.LineStrips2D#radii")?
            })
        } else {
            None
        };
        let colors = if let Some(array) = arrays_by_name.get("colors") {
            Some({
                <crate::components::Color>::try_from_arrow_opt(&**array)
                    .with_context("rerun.archetypes.LineStrips2D#colors")?
                    .into_iter()
                    .map(|v| v.ok_or_else(crate::DeserializationError::missing_data))
                    .collect::<crate::DeserializationResult<Vec<_>>>()
                    .with_context("rerun.archetypes.LineStrips2D#colors")?
            })
        } else {
            None
        };
        let labels = if let Some(array) = arrays_by_name.get("labels") {
            Some({
                <crate::components::Label>::try_from_arrow_opt(&**array)
                    .with_context("rerun.archetypes.LineStrips2D#labels")?
                    .into_iter()
                    .map(|v| v.ok_or_else(crate::DeserializationError::missing_data))
                    .collect::<crate::DeserializationResult<Vec<_>>>()
                    .with_context("rerun.archetypes.LineStrips2D#labels")?
            })
        } else {
            None
        };
        let draw_order = if let Some(array) = arrays_by_name.get("draw_order") {
            Some({
                <crate::components::DrawOrder>::try_from_arrow_opt(&**array)
                    .with_context("rerun.archetypes.LineStrips2D#draw_order")?
                    .into_iter()
                    .next()
                    .flatten()
                    .ok_or_else(crate::DeserializationError::missing_data)
                    .with_context("rerun.archetypes.LineStrips2D#draw_order")?
            })
        } else {
            None
        };
        let class_ids = if let Some(array) = arrays_by_name.get("class_ids") {
            Some({
                <crate::components::ClassId>::try_from_arrow_opt(&**array)
                    .with_context("rerun.archetypes.LineStrips2D#class_ids")?
                    .into_iter()
                    .map(|v| v.ok_or_else(crate::DeserializationError::missing_data))
                    .collect::<crate::DeserializationResult<Vec<_>>>()
                    .with_context("rerun.archetypes.LineStrips2D#class_ids")?
            })
        } else {
            None
        };
        let instance_keys = if let Some(array) = arrays_by_name.get("instance_keys") {
            Some({
                <crate::components::InstanceKey>::try_from_arrow_opt(&**array)
                    .with_context("rerun.archetypes.LineStrips2D#instance_keys")?
                    .into_iter()
                    .map(|v| v.ok_or_else(crate::DeserializationError::missing_data))
                    .collect::<crate::DeserializationResult<Vec<_>>>()
                    .with_context("rerun.archetypes.LineStrips2D#instance_keys")?
            })
        } else {
            None
        };
        Ok(Self {
            strips,
            radii,
            colors,
            labels,
            draw_order,
            class_ids,
            instance_keys,
        })
    }
}

impl LineStrips2D {
    pub fn new(
        strips: impl IntoIterator<Item = impl Into<crate::components::LineStrip2D>>,
    ) -> Self {
        Self {
            strips: strips.into_iter().map(Into::into).collect(),
            radii: None,
            colors: None,
            labels: None,
            draw_order: None,
            class_ids: None,
            instance_keys: None,
        }
    }

    pub fn with_radii(
        mut self,
        radii: impl IntoIterator<Item = impl Into<crate::components::Radius>>,
    ) -> Self {
        self.radii = Some(radii.into_iter().map(Into::into).collect());
        self
    }

    pub fn with_colors(
        mut self,
        colors: impl IntoIterator<Item = impl Into<crate::components::Color>>,
    ) -> Self {
        self.colors = Some(colors.into_iter().map(Into::into).collect());
        self
    }

    pub fn with_labels(
        mut self,
        labels: impl IntoIterator<Item = impl Into<crate::components::Label>>,
    ) -> Self {
        self.labels = Some(labels.into_iter().map(Into::into).collect());
        self
    }

    pub fn with_draw_order(mut self, draw_order: impl Into<crate::components::DrawOrder>) -> Self {
        self.draw_order = Some(draw_order.into());
        self
    }

    pub fn with_class_ids(
        mut self,
        class_ids: impl IntoIterator<Item = impl Into<crate::components::ClassId>>,
    ) -> Self {
        self.class_ids = Some(class_ids.into_iter().map(Into::into).collect());
        self
    }

    pub fn with_instance_keys(
        mut self,
        instance_keys: impl IntoIterator<Item = impl Into<crate::components::InstanceKey>>,
    ) -> Self {
        self.instance_keys = Some(instance_keys.into_iter().map(Into::into).collect());
        self
    }
}
