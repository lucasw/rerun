// DO NOT EDIT!: This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs:54.
// Based on "crates/re_types/definitions/rerun/archetypes/disconnected_space.fbs".

#include "disconnected_space.hpp"

#include "../components/disconnected_space.hpp"

namespace rerun {
    namespace archetypes {
        Result<std::vector<rerun::DataCell>> DisconnectedSpace::to_data_cells() const {
            std::vector<rerun::DataCell> cells;
            cells.reserve(1);

            {
                const auto result =
                    rerun::components::DisconnectedSpace::to_data_cell(&disconnected_space, 1);
                if (result.is_err()) {
                    return result.error;
                }
                cells.emplace_back(std::move(result.value));
            }
            {
                const auto result = create_indicator_component(
                    "rerun.components.DisconnectedSpaceIndicator",
                    num_instances()
                );
                if (result.is_err()) {
                    return result.error;
                }
                cells.emplace_back(std::move(result.value));
            }

            return cells;
        }
    } // namespace archetypes
} // namespace rerun
