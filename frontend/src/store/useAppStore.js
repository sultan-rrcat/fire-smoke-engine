import { create } from "zustand";

const useAppStore = create((set) => ({
    videoId: null,
    processing: false,
    results: null,

    setVideoId: (id) => set({ videoId: id }),
    setProcessing: (status) => set({ processing: status }),
    setResults: (results) => set({ results })
}));

export default useAppStore;