import React, { useState } from "react";
import Layout from "../layouts/Search";
import { useRouter } from "next/router";
import fetch from "isomorphic-unfetch";

function useSearch(initialResults) {
  const [results, setResults] = useState(initialResults);
  const [loading, setLoading] = useState(false);

  return {
    results,
    loading,
    search: (query: string) => {
      setLoading(true);
      fetch(process.env.BACKEND + `/v1/search?q=${query}`)
        .then((res) => res.json())
        .then(setResults)
        .finally(() => setLoading(false));
    },
  };
}

export default function Search({ results: initialResults }) {
  const { results, search, loading } = useSearch(initialResults);
  const router = useRouter();

  return (
    <Layout
      {...{ loading, results }}
      getResults={async (query) => {
        router.push(`/search?q=${query}`);
        search(query);
      }}
    />
  );
}

Search.getInitialProps = async (ctx) => {
  const { q: query } = ctx.query;
  const results = await fetch(
    process.env.BACKEND + `/v1/search?q=${encodeURIComponent(query)}`
  ).then((res) => res.json());
  return { results, query };
};
