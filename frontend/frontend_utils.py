#frontend/utils.py
import streamlit as st
import pandas as pd
def display_comparison_table(comparison_data):
    """Render side-by-side comparison table of two channels."""
    if not isinstance(comparison_data, list):
        st.error("❌ Expected a list of channel data, got something else.")
        return

    safe_data = []
    for idx, item in enumerate(comparison_data):
        if not isinstance(item, dict):
            st.warning(f"⚠️ Skipping invalid item: {item}")
            continue
        channel = item.copy()
        channel.setdefault("channel_name", f"Channel {idx + 1}")
        safe_data.append(channel)

    if not safe_data:
        st.error("❌ No valid channel data found.")
        return

    df = pd.DataFrame(safe_data)
    if "channel_name" not in df.columns:
        st.error("❌ 'channel_name' not found in data.")
        return

    df.set_index("channel_name", inplace=True)
    st.dataframe(df.T)



def plot_bar_comparison(comparison_data, metric="subscribers"):
    """Plot a bar chart comparing selected metric between channels."""
    # Handle case where data is wrapped in a dict
    if isinstance(comparison_data, dict) and "comparisons" in comparison_data:
        comparison_data = comparison_data["comparisons"]

    labels = [d["channel_name"] for d in comparison_data]
    values = [int(d.get(metric, 0)) for d in comparison_data]
    chart_data = pd.DataFrame({metric.title(): values}, index=labels)
    st.bar_chart(chart_data)
