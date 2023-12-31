/* eslint-disable camelcase */
export type Project = {
    name: string;
};

export type Credentials = {
    name: string;
    url: string;
};

export type Version = {
    number: number;
    description: string;
    id: number;
    created_at: string;
    updated_at: string;
    org_units_count: number;
};

export type DataSource = {
    name: string;
    read_only: boolean;
    description: string;
    versions: Version[];
    url: string;
    projects: Project[];
    default_version: Version;
    credentials: Credentials;
};
