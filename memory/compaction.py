from langchain_core.chat_history import InMemoryChatMessageHistory


def compact_consecutive_messages(history: InMemoryChatMessageHistory):
    if not history.messages:
        return

    compacted_message_dicts = []

    for current_message_dict in history.messages:
        if (
            not isinstance(current_message_dict, dict)
            or 'role' not in current_message_dict
        ):
            print(
                f'Skipping message with unexpected format during compaction: {type(current_message_dict)} - {current_message_dict}'
            )
            continue

        current_role = current_message_dict.get('role')
        current_content = current_message_dict.get('content', '')

        if not current_role:
            print(
                f'Skipping message with missing role during compaction: {current_message_dict}'
            )
            continue

        if (
            compacted_message_dicts
            and compacted_message_dicts[-1]['role'] == current_role
        ):
            if isinstance(current_content, str):
                compacted_message_dicts[-1][
                    'content'
                ] += f'\n{current_content}'
            else:
                compacted_message_dicts[-1][
                    'content'
                ] += f'\n{str(current_content)}'
        else:
            new_message_entry = {
                'role': current_role,
                'content': current_content,
            }
            for key, value in current_message_dict.items():
                if key not in new_message_entry:
                    new_message_entry[key] = value
            compacted_message_dicts.append(new_message_entry)

    history.messages = compacted_message_dicts
