// DO NOT EDIT!: This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs:54.
// Based on "crates/re_types/definitions/rerun/testing/datatypes/fuzzy.fbs".

#include "affix_fuzzer20.hpp"

#include "primitive_component.hpp"
#include "string_component.hpp"

#include <arrow/builder.h>
#include <arrow/type_fwd.h>

namespace rerun {
    namespace datatypes {
        const std::shared_ptr<arrow::DataType> &AffixFuzzer20::arrow_datatype() {
            static const auto datatype = arrow::struct_({
                arrow::field("p", rerun::datatypes::PrimitiveComponent::arrow_datatype(), false),
                arrow::field("s", rerun::datatypes::StringComponent::arrow_datatype(), false),
            });
            return datatype;
        }

        Result<std::shared_ptr<arrow::StructBuilder>> AffixFuzzer20::new_arrow_array_builder(
            arrow::MemoryPool *memory_pool
        ) {
            if (!memory_pool) {
                return Error(ErrorCode::UnexpectedNullArgument, "Memory pool is null.");
            }

            return Result(std::make_shared<arrow::StructBuilder>(
                arrow_datatype(),
                memory_pool,
                std::vector<std::shared_ptr<arrow::ArrayBuilder>>({
                    rerun::datatypes::PrimitiveComponent::new_arrow_array_builder(memory_pool)
                        .value,
                    rerun::datatypes::StringComponent::new_arrow_array_builder(memory_pool).value,
                })
            ));
        }

        Error AffixFuzzer20::fill_arrow_array_builder(
            arrow::StructBuilder *builder, const AffixFuzzer20 *elements, size_t num_elements
        ) {
            if (!builder) {
                return Error(ErrorCode::UnexpectedNullArgument, "Passed array builder is null.");
            }
            if (!elements) {
                return Error(
                    ErrorCode::UnexpectedNullArgument,
                    "Cannot serialize null pointer to arrow array."
                );
            }

            {
                auto field_builder = static_cast<arrow::UInt32Builder *>(builder->field_builder(0));
                ARROW_RETURN_NOT_OK(field_builder->Reserve(static_cast<int64_t>(num_elements)));
                for (size_t elem_idx = 0; elem_idx < num_elements; elem_idx += 1) {
                    RR_RETURN_NOT_OK(rerun::datatypes::PrimitiveComponent::fill_arrow_array_builder(
                        field_builder,
                        &elements[elem_idx].p,
                        1
                    ));
                }
            }
            {
                auto field_builder = static_cast<arrow::StringBuilder *>(builder->field_builder(1));
                ARROW_RETURN_NOT_OK(field_builder->Reserve(static_cast<int64_t>(num_elements)));
                for (size_t elem_idx = 0; elem_idx < num_elements; elem_idx += 1) {
                    RR_RETURN_NOT_OK(rerun::datatypes::StringComponent::fill_arrow_array_builder(
                        field_builder,
                        &elements[elem_idx].s,
                        1
                    ));
                }
            }
            ARROW_RETURN_NOT_OK(builder->AppendValues(static_cast<int64_t>(num_elements), nullptr));

            return Error::ok();
        }
    } // namespace datatypes
} // namespace rerun
