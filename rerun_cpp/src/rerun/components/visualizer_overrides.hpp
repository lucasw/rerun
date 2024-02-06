// DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/re_types/definitions/rerun/components/visualizer_overrides.fbs".

#pragma once

#include "../collection.hpp"
#include "../result.hpp"

#include <cstdint>
#include <memory>
#include <string>
#include <utility>

namespace arrow {
    class Array;
    class DataType;
    class ListBuilder;
} // namespace arrow

namespace rerun::components {
    /// **Component**: The name of a visualizer.
    struct VisualizerOverrides {
        rerun::Collection<std::string> value;

      public:
        VisualizerOverrides() = default;

        VisualizerOverrides(rerun::Collection<std::string> value_) : value(std::move(value_)) {}

        VisualizerOverrides& operator=(rerun::Collection<std::string> value_) {
            value = std::move(value_);
            return *this;
        }
    };
} // namespace rerun::components

namespace rerun {
    template <typename T>
    struct Loggable;

    /// \private
    template <>
    struct Loggable<components::VisualizerOverrides> {
        static constexpr const char Name[] = "rerun.components.VisualizerOverrides";

        /// Returns the arrow data type this type corresponds to.
        static const std::shared_ptr<arrow::DataType>& arrow_datatype();

        /// Fills an arrow array builder with an array of this type.
        static rerun::Error fill_arrow_array_builder(
            arrow::ListBuilder* builder, const components::VisualizerOverrides* elements,
            size_t num_elements
        );

        /// Serializes an array of `rerun::components::VisualizerOverrides` into an arrow array.
        static Result<std::shared_ptr<arrow::Array>> to_arrow(
            const components::VisualizerOverrides* instances, size_t num_instances
        );
    };
} // namespace rerun